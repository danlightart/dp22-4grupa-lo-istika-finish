window.addEventListener("load", function(){
    getPosts();
})

async function getPosts(){
    let response = await fetch('/data')
    let data = await response.json()

    let posts = document.getElementById('posts')
    posts.innerHTML = ""

    for(let post of data){
            /* Jaunu produktu paradīšana. */
            
        postsHTML = `<div><img id="phones" class="image" src="${post.img}"><h2 id="text"><b>Modelis: </b>${post.model}</h2><h2 id="text"><b>Cena: </b>${post.cost}</h2><div class="button" id="text"><a href="/panel/delete/${post.id}">Delete</a></div>`
        posts.innerHTML = posts.innerHTML + postsHTML
    }
}