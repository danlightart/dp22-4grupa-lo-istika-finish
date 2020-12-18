window.addEventListener("load", function(){
    getPosts();
})

async function getPosts(){
    let response = await fetch('/data')
    let data = await response.json()

    let posts = document.getElementById('posts')
    posts.innerHTML = ""

    for(let post of data){

            postsHTML = `<li><div class="border"><img id="phones" class="image" src="${post.img}"><h2><b>Modelis: </b>${post.model}</h2><h2><b>Cena: </b>${post.cost}</h2><div class="button"><a href="/findproduct/phones/buy/${post.id}">Buy now</a></div></div></li>`
            posts.innerHTML = posts.innerHTML + postsHTML
    }
}