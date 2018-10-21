/*** 
 * script to toggle accordion links on the winners index page
 */

const wards = document.querySelectorAll(".wrv-accordion a");

function toggleAccordion(){
    this.classList.toggle('active');
    this.nextElementSibling.classList.toggle('active');
}

wards.forEach(ward => ward.addEventListener('click', toggleAccordion));