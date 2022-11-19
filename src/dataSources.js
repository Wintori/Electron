const template = document.querySelector(".data-template").content

function createCard (name, type, lastChange, status) {
    console.log(template)
    console.log(template.querySelector(".information__data-source__item"))
    const post = template.querySelector(".information__data-source__item").cloneNode(true)
    const postName = post.querySelector(".information__data-source__item-name")
    const postType = post.querySelector(".information__data-source__item-type")
    const postChange = post.querySelector(".information__data-source__item-change")
    const postStatus = post.querySelector(".information__data-source__item-status")

    postName.textContent = name
    postType.textContent = type
    postChange.textContent = lastChange
    postStatus.textContent = status

    return post
}

const example = createCard("Todos", "JSON", "18.11.22", "подключено")
document.querySelector(".information__data-source").append(example)