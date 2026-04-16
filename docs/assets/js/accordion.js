/***
 * script to toggle accordion links on the winners index page
 */


function toggleAccordion(){
    var targetId = this.getAttribute("aria-controls");
    var target = targetId ? document.getElementById(targetId) : this.nextElementSibling;
    var isExpanded = this.getAttribute("aria-expanded") === "true";

    if (!target) {
      return;
    }

    this.classList.toggle('active', !isExpanded);
    this.setAttribute("aria-expanded", String(!isExpanded));
    target.hidden = isExpanded;
    target.classList.toggle('active', !isExpanded);
}

const toggles = document.querySelectorAll(".toggletop");
toggles.forEach(toggles => toggles.addEventListener('click', toggleAccordion));
