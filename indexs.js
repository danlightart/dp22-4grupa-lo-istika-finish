window.addEventListener("load", function(){
    getUsers()
})

async function getUsers(){
    let response = await fetch('/users')
    let data_json = await response.json()
   
    let users = document.getElementById('users')
    users.innerHTML = ''

    for(let user of data_json){
        msgHTML = `<p>Vārds:${user.vards} Uzvārds:${user.uzvards}</p><button onclick="editUser('${user._id.$oid}')">Edit</button>`
        users.innerHTML = users.innerHTML + msgHTML
    }
}

async function editUser(id){
    let response = await fetch(`/user/${id}`)
    let data = await response.json()

    console.log(data)
}