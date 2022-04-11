const menu = document.querySelector('#menu-bars');
const navbar = document.querySelector('.navbar');
const searchIcon = document.querySelector('#search-icon');
const searchForm = document.querySelector('.searchform');



menu.onclick = () => {
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
    searchIcon.classList.remove('fa-times');
    searchForm.classList.remove('active');
}

searchIcon.onclick = () => {
    searchIcon.classList.toggle('fa-times');
    searchForm.classList.toggle('active');
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');
}

window.onscroll = () => {
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');
    searchIcon.classList.remove('fa-times');
    searchForm.classList.remove('active');
}