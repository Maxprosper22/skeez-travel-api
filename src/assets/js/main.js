import anime from 'animejs/lib/anime.es.js';

const target = document.querySelector('#target');

anime({
    targets: target,
    translateX: 250,
    rotate: '1turn',
    duration: 2000,
    easing: 'easeInOutQuad',
    loop: true
});
