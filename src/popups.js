function myFunction() {
    document.getElementById("myPopup").classList.add("popup__content_show");
}
window.onclick = function(event) {
    if (!event.target.matches('.popup__img')) {
        let dropdowns = document.getElementsByClassName("popup__content");
        for (let i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('popup__content_show')) {
                openDropdown.classList.remove('popup__content_show');
            }
        }
    }
}
