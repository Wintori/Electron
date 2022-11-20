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



const templateGroup = document.querySelector(".group-template").content
const templateApi = document.querySelector(".api-template").content
const groupLink = document.getElementById('group')
const apiLink = document.getElementById('api')
const elementsList = document.querySelectorAll(".information__groups__item")
const elementsListArray = Array.from(elementsList)

function removeAllCards () {
    document.querySelectorAll(".information__groups__item").forEach((element) => {
        element.remove()
    })
}

function createCardTemplate (name) {
    const post = templateGroup.querySelector(".information__groups__item").cloneNode(true)
    const postName = post.querySelector(".information__groups__text")

    postName.textContent = name
    return post
}

function createCardApi (name, host) {
    const post = templateApi.querySelector(".information__api__item").cloneNode(true)
    const postName = post.querySelector(".information__api__key")
    const postHost = post.querySelector(".information__api__host")

    postName.textContent = name
    postHost.textContent = host
    return post
}

function renderCard(card) {
    document.querySelector(".information__groups").append(card)
}

function renderCardApi(card) {
    document.querySelector(".information__api").append(card)
}

function groupLinkHandler () {
    if (document.querySelector('.information__groups')) {
        document.querySelector('.information__groups').remove();
    }
    if (document.querySelector('.information__api')) {
        document.querySelector('.information__api').remove();
    }


    const newUl = document.createElement("ul");
    newUl.classList.add('information__groups');
    (document.querySelector('.information')).appendChild(newUl);

    renderCard(createCardTemplate('Группа 1'))
    renderCard(createCardTemplate('Группа 2'))
    renderCard(createCardTemplate('Группа 3'))
    renderCard(createCardTemplate('Группа 4'))

}


function apiLinkHandler () {
    let count = 1
    if (document.querySelector('.information__groups')) {
        document.querySelector('.information__groups').remove();
    }
    if (document.querySelector('.information__api')) {
        document.querySelector('.information__api').remove();
    }

    const newUl = document.createElement("ul");
    newUl.classList.add('information__api');
    (document.querySelector('.information')).appendChild(newUl);

    renderCardApi(createCardApi(`${count}. NameApi`, 'exampleHost.com'))
    count++;
    renderCardApi(createCardApi(`${count}. NameApi`, 'exampleHost.com'))
    count++;
    renderCardApi(createCardApi(`${count}. NameApi`, 'exampleHost.com'))

}

groupLink.addEventListener('click', groupLinkHandler)
apiLink.addEventListener('click', apiLinkHandler)

groupLinkHandler()