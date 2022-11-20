const template = document.querySelector(".data-template").content

function createCard (name, type, lastChange, status) {
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

const example = createCard("Todos", "JSON", "18.11.2022", "подключено")
document.querySelector(".information__data-source").append(example)
const example1 = createCard("FFFFFFFFF", "TEST", "10.11.2022", "подключено")
document.querySelector(".information__data-source").append(example1)
const example2 = createCard("TEST", "LOREMIPSUM", "01.01.2022", "подключено")
document.querySelector(".information__data-source").append(example2)
const example3 = createCard("UNO", "DOS", "18.11.2022", "подключено")
document.querySelector(".information__data-source").append(example3)
