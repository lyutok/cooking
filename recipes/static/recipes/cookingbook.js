document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const parts = path.split('/');
    const category = parts[parts.length - 1];
    console.log(category);

    main(category);
});


async function get_data(category) {
    const response = await fetch('/allrecipes');
    const data = await response.json();
    console.log(data);

    // Filter the data by category
    const filteredData = data.filter(item => item.category === category);
    console.log(filteredData);
    return filteredData;
}


async function main(category) {
    // Check if user logged in
    const isAuthenticated = document.body.getAttribute('data-authenticated') === 'True';
    // Get data from server to show
    let data = await get_data(category);
    let rows = Math.ceil(data.length / 3);
    console.log("rows: ", rows);
    let img_link = "";
    let title = "";
    let like = "";
    let y = 0;

    // Get the cards-row-template
    for (let i = 0; i < rows; i++) {

        const rowTemplate = document.getElementById('cards-row-template');
        const rowClone = rowTemplate.content.cloneNode(true);

        const cardTemplate = rowClone.querySelector('#card-template');

        for (let i = 0; i < 3; i++) {
            console.log("y: ", y);
            if (y < data.length) {
                visibility = "block";
                img_link = '/media/' + data[y]["image"];
                title = data[y]["title"];
                like = data[y]["favorite"] ? "❤️" : "🤍";
                edit = "Edit";
                description = data[y]["description"]
                id = data[y]["id"]
            } else {
                visibility = "none";
                title = "";
                like = "";
                edit = "";
            }
            y += 1;

            const cardClone = cardTemplate.content.cloneNode(true);

            // Modify elements in the clone: title, image, button
            const title_element = cardClone.querySelector('.sub-title');
            title_element.innerText = title;
            console.log("title", title);

            const image_element = cardClone.querySelector('.food-img');
            image_element.style.display = visibility;
            image_element.src = img_link;
            console.log("img_link", img_link);

            const recipe_element = cardClone.querySelector('.recipe');
            recipe_element.innerText = description;

            image_element.addEventListener('click', function() {

                if (this.classList.contains('fade-in')) {
                    this.classList.remove('fade-in');
                    this.classList.add('fade-out');
                    recipe_element.style.display = "block";
                } else {
                    this.classList.remove('fade-out');
                    this.classList.add('fade-in');
                    recipe_element.style.display = "none";
                }
            });

            const buttons_row = cardClone.querySelector('.buttons');
            buttons_row.setAttribute('id', id);

            if (isAuthenticated) {
                const like_element = cardClone.querySelector('.like-bttn');
                like_element.innerText = like;

                like_element.addEventListener('click', function() {
                    // like_update
                    if (this.innerText === "❤️") {
                        this.innerText = "🤍";
                        isLike = false;
                    } else {
                        this.innerText = "❤️";
                        isLike = true;
                    }
                    like_update(buttons_row.id, isLike);
                });

                // Edit button
                const edit_element = cardClone.querySelector('.btn-light');
                edit_element.innerText = edit;
                edit_element.setAttribute('href', `/recipes_edit/${id}`);

                console.log(id);

                if (visibility === "none") {
                    edit_element.style.visibility = "hidden";
                } else {
                    edit_element.style.visibility = "visible";
                }
            }
            rowClone.querySelector('.card-container').appendChild(cardClone);
        }
        // Append the final row to the row-container
        document.querySelector('#row-container').appendChild(rowClone);
    }
}


function like_update(id, isLike) {
    console.log(id, isLike);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch(`/allrecipes?id=${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            favorite: isLike,
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text); });
        }
        return response.json();
    })
    .then(data => {
        console.log('Successfully updated follower status:', data);
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}
