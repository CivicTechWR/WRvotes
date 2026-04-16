/***
 * Keep the ward race tabs keyboard- and screen-reader-friendly.
 */

$(document).ready(function() {
  function getRadioForTab(tab) {
    return document.getElementById(tab.getAttribute("for"));
  }

  function syncTabs(nav) {
    nav.querySelectorAll('[role="tab"]').forEach(function(tab) {
      var radio = getRadioForTab(tab);
      var isSelected = radio ? radio.checked : false;
      tab.setAttribute("aria-selected", String(isSelected));
      tab.setAttribute("tabindex", isSelected ? "0" : "-1");

      var controlledId = tab.getAttribute("aria-controls");
      if (!controlledId) {
        return;
      }

      var controlledElement = document.getElementById(controlledId);
      if (!controlledElement) {
        return;
      }

      if (controlledElement.getAttribute("role") === "tabpanel") {
        controlledElement.setAttribute(
          "aria-hidden",
          String(window.getComputedStyle(controlledElement).display === "none"),
        );
      } else {
        controlledElement.setAttribute("aria-hidden", String(!isSelected));
      }
    });
  }

  function selectTab(tab, shouldFocus) {
    var radio = getRadioForTab(tab);
    var nav = tab.closest("nav#toc-tabs");

    if (!radio || !nav) {
      return;
    }

    radio.checked = true;
    syncTabs(nav);

    if (shouldFocus) {
      tab.focus();
    }
  }

  document.querySelectorAll("nav#toc-tabs").forEach(function(nav) {
    syncTabs(nav);

    nav.querySelectorAll('[role="tab"]').forEach(function(tab) {
      tab.addEventListener("click", function() {
        window.requestAnimationFrame(function() {
          syncTabs(nav);
        });
      });

      tab.addEventListener("keydown", function(event) {
        var tablist = tab.closest('[role="tablist"]');
        var tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
        var currentIndex = tabs.indexOf(tab);
        var targetTab = null;

        if (event.key === "ArrowRight") {
          targetTab = tabs[(currentIndex + 1) % tabs.length];
        } else if (event.key === "ArrowLeft") {
          targetTab = tabs[(currentIndex - 1 + tabs.length) % tabs.length];
        } else if (event.key === "Home") {
          targetTab = tabs[0];
        } else if (event.key === "End") {
          targetTab = tabs[tabs.length - 1];
        } else if (event.key === " " || event.key === "Enter") {
          targetTab = tab;
        }

        if (!targetTab) {
          return;
        }

        event.preventDefault();
        selectTab(targetTab, true);
      });
    });

    nav.parentElement.querySelectorAll(".tab-radio").forEach(function(radio) {
      radio.addEventListener("change", function() {
        syncTabs(nav);
      });
    });
  });
});
