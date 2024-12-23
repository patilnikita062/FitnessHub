// let element = document.getElementById('btn')
// element.addEventListener('click', hire_me);
// function hire_me() {
//     let displayy = document.getElementById('hire');
//     displayy.style.display = 'block'
// }
let home = document.getElementById('home');
home.addEventListener('click', back);
function back() {
    location.reload();
    document.getElementById('line').style.display = 'block'
}
