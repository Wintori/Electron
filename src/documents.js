const template = document.querySelector(".card-template").content
const templateLink = document.getElementById('template')
const reportLink = document.getElementById('report')
const exportLink = document.getElementById('export')
const elementsList = document.querySelectorAll(".information__documents__item")
const elementsListArray = Array.from(elementsList)


function createCardTemplate (name, size, date, type) {
    const post = template.querySelector(".information__documents__item").cloneNode(true)
    const postName = post.querySelector(".information__documents__name")
    const postImg = post.querySelector(".information__documents__img")
    const postSize = post.querySelector(".information__documents__size")
    const postDate = post.querySelector(".information__documents__date")

    switch (type) {
        case 0: postImg.src = "./images/document.svg"; break;
        case 1: postImg.src = "./images/file-icon.svg"; break;
        case 2: postImg.src = "./images/document.svg"; break;
    }

    postImg.alt = name
    postName.textContent = name
    postSize.textContent = size
    postDate.textContent = date

    return post
}

function renderCard(card) {
    document.querySelector(".information__documents").append(card)
}

const example = createCardTemplate("Todos", "42100", "18.11.2022", 1)
document.querySelector(".information__documents").append(example)

const example1 = createCardTemplate("TEST1", "12345", "01.01.2022", 0)
document.querySelector(".information__documents").append(example1)



const asideList = document.querySelector('.aside-menu__list')
const asideItems = asideList.querySelectorAll('.aside-menu__item')
const asideItemsArray = Array.from(asideItems)

closeAllTabs = () => {
    asideItemsArray.forEach((item) => {
        item.classList.remove('aside-menu__item_active')
        item.querySelector('.aside-menu__img').classList.remove('aside-menu__img_active')
        item.querySelector('.aside-menu__text').classList.remove('aside-menu__text_active')
    })
}

setTabActiveHandler = (element) => {
    if (!element.classList.contains('aside-menu__item_active')) {
        closeAllTabs()
        element.classList.add('aside-menu__item_active')
        element.querySelector('.aside-menu__img').classList.add('aside-menu__img_active')
        element.querySelector('.aside-menu__text').classList.add('aside-menu__text_active')
    }
}



asideItemsArray.forEach((asideElement) => {
    asideElement.addEventListener("click", () => {
        setTabActiveHandler(asideElement)
    })
})

function removeAllCards () {
    document.querySelectorAll(".information__documents__item").forEach((element) => {
        element.remove()
    })
}

function templateLinkHandler () {
    removeAllCards()
    renderCard(createCardTemplate('TEST', '6709', '01.07.2022', 0))
    renderCard(createCardTemplate('LOREMIPSUM', '1045', '01.12.2022', 1))
    renderCard(createCardTemplate('MKDIR', '3100', '28.09.2019', 1))
}

function reportLinkHandler () {
    removeAllCards()
    renderCard(createCardTemplate('TEST', '6709', '01.07.2022', 0))
    renderCard(createCardTemplate('LOREMIPSUM', '1045', '01.12.2022', 1))
    renderCard(createCardTemplate('MKDIR', '3100', '28.09.2019', 1))
    renderCard(createCardTemplate('TEST', '6709', '01.07.2022', 1))
    renderCard(createCardTemplate('LOREMIPSUM', '1045', '01.12.2022', 1))
    renderCard(createCardTemplate('MKDIR', '3100', '28.09.2019', 1))
    renderCard(createCardTemplate('TEST', '6709', '01.07.2022', 0))
    renderCard(createCardTemplate('LOREMIPSUM', '1045', '01.12.2022', 1))
    renderCard(createCardTemplate('MKDIR', '3100', '28.09.2019', 1))
    renderCard(createCardTemplate('TEST', '6709', '01.07.2022', 1))
    renderCard(createCardTemplate('LOREMIPSUM', '1045', '01.12.2022', 1))
    renderCard(createCardTemplate('MKDIR', '3100', '28.09.2019', 1))
}

function exportLinkHandler () {
    removeAllCards()
    renderCard(createCardTemplate('TEST', '6709', '01.07.2022', 1))
    renderCard(createCardTemplate('LOREMIPSUM', '1045', '01.12.2022', 1))
    renderCard(createCardTemplate('MKDIR', '3100', '28.09.2019', 1))
    renderCard(createCardTemplate('TEST', '6709', '01.07.2022', 0))
    renderCard(createCardTemplate('LOREMIPSUM', '1045', '01.12.2022', 1))
    renderCard(createCardTemplate('MKDIR', '3100', '28.09.2019', 1))
    renderCard(createCardTemplate('TEST', '6709', '01.07.2022', 1))
}

templateLink.addEventListener('click', templateLinkHandler)
reportLink.addEventListener('click', reportLinkHandler)
exportLink.addEventListener('click', exportLinkHandler)
