const btn = document.getElementById('menu-btn');
const menu = document.getElementById('mobile-menu');

btn.addEventListener('click', () => {
    menu.classList.toggle('hidden');
});

let currIndex = 0;

function showSlide(index) {
    const items = document.querySelectorAll('.carousel-item');
    items.forEach((item, i) => {
        item.classList.toggle('hidden', i !== index);
    });
}

function nextSlide() {
    const items = document.querySelectorAll('.carousel-item');
    currIndex = (currIndex + 1) % items.length;
    showSlide(currIndex);
}

function prevSlide() {
    const items = document.querySelectorAll('.carousel-item');
    currIndex = (currIndex - 1 + items.length) % items.length;
    showSlide(currIndex);
}

document.addEventListener('DOMContentLoaded', () => {
    showSlide(currIndex);
    Fancybox.bind("[data-fancybox='gallery']");
});
