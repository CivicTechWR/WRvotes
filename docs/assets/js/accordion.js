/***
 * script to toggle accordion links on the winners index page
 */


function toggleAccordion(){
    this.classList.toggle('active');

    // Sigh. Maybe I want some elements in between.
    curr  = this.nextElementSibling;
    while (curr) { 
      if (curr.classList.contains("toggle-content")) { 
         target = curr;
         break;
      } 
      curr = curr.nextElementSibling;

    } // end while

    target.classList.toggle('active');
}

const toggles = document.querySelectorAll(".toggletop");
toggles.forEach(toggles => toggles.addEventListener('click', toggleAccordion));
