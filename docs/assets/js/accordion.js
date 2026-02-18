/***
 * script to toggle accordion links on the winners index page
 */


function toggleAccordion(){
    this.classList.toggle('active');
    this.nextElementSibling.classList.toggle('active');
}

const toggles = document.querySelectorAll(".toggleable");
toggles.forEach(toggles => toggles.addEventListener('click', toggleAccordion));
