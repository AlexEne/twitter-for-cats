console.log("Hello world!")


const form = document.querySelector('form');
const loadingElement = document.querySelector('.loading');
const API_URL = "http://127.0.0.1:5000/postmew" //?name=test&mew=mewmew
const mewsElement = document.querySelector('.mews');

loadingElement.style.display = 'none';

listAllMews();

form.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const name = formData.get("name");
    const content = formData.get("content");

    const mew = {
        name,
        content
    };

    console.log(mew);
    loadingElement.style.display = '';
    form.style.display = 'none';

    fetch(API_URL, {
        method: 'POST',
        body: JSON.stringify(mew),
        headers: {
            'content-type': 'application/json'
        }
    }).then(function (response) {
        setTimeout(() => {
            loadingElement.style.display = 'none';
            form.style.display = '';
            form.reset();
            listAllMews();
        }, 300);

    });
});


function listAllMews() {
    mewsElement.innerHTML = '';

    fetch("http://127.0.0.1:5000/mews")
        .then(response => response.json())
        .then(mews => {
            mews.forEach(mew => {
                mew.date = Date.parse(mew.Date);
            });

            mews.sort(function (a, b) {
                return new Date(b.date) - new Date(a.date);
            });

            mews.forEach(mew => {
                const div = document.createElement('div');
                const header = document.createElement('h3');
                header.textContent = mew.Name;
                const contents = document.createElement('p');
                contents.textContent = mew.Mew;

                const date = document.createElement('small');
                date.textContent = new Date(Date.parse(mew.Date));

                div.appendChild(header);
                div.appendChild(date);
                div.appendChild(contents);

                mewsElement.appendChild(div);
            });
        })
}