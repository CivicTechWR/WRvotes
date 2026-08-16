/***
 * Helper scripts to show/hide elements of candidate lists.
 * (This was not the highest priority item...)
 */

$(document).ready(function () {
  var WIDESCREEN = 1100;

  /* Compute a button label based upon the classes
   * in a particular ID.
   */
  function get_description(id) {
    var desc = "Items";

    if ($(id).attr('title') !== undefined) { 
      desc = $(id).attr('title');
    } else if ($(id).hasClass("candidate-list")) {
      desc = "This Listing";
    } else if ($(id).hasClass("electionresult-list")) {
      desc = "Election Results";
    } else if ($(id).hasClass("event-list")) {
      desc = "Events";
    } else if ($(id).hasClass("news-list")) {
      desc = "News Items";
    } else if ($(id).hasClass("background")) {
      desc = "Background";
    }

    return desc;
  } // get_description

  // ------------------------
  function add_toggle_button() {
    var target = $(this).attr("id");
    var classes = $(this).attr("class").split(/\s+/);
    // Convert js-hidden to hidden
    const hidden_loc = classes.indexOf("js-hidden");
    if (hidden_loc > -1) { 
      classes.splice(hidden_loc, 1);
      classes.push("hidden");  

      $(this).addClass("hidden");
      $(this).removeClass("js-hidden");
    } 


    var toggle_button_cls = "toggle-button";

    var show_more_text = "Show More";
    var show_fewer_text = "Show Fewer";
    var inittext = show_more_text;
    var target_button_id =  target + "-btn";
    var target_button_hash = "#" + target_button_id;
    var arrow = " ▼";

    var desc = get_description("#" + target);
    /* 
    if (hasAttribute("desc") { 
      desc = $(this).attr("desc");
    }
    */

    if (classes.includes("media-toggle")) { 
      show_more_text = $(this).attr("show_more_text");
      show_fewer_text = $(this).attr("show_fewer_text");

      if (classes.includes("hidden")) { 
        arrow = " ▼";
        inittext = show_more_text;
      } else { 
        arrow = " ▲";
        inittext = show_fewer_text;
      }
    } 

    if (classes.includes("background")) {
      toggle_button_cls = "toggle-button-background";
    }

    var classes_to_add = "";
    // Ugh. Remove "togglable" from the list of
    // classes to add to the button.
    for (var i = 0; i < classes.length; i++) {
      if (classes[i] !== "togglable") {
        classes_to_add = classes_to_add + " " + classes[i];
      } // endif
    } // end for

    retval =
      `<button data-ul="${target}"` +
      ` id="${target_button_id}"` +
      ` class="${toggle_button_cls} v04 ${target} ${classes_to_add}" >` +
      ` ${inittext} ${desc} ${arrow}` + 
      "</button>";
    $(this).parent().append(retval);


    // Initialize listener
    $(target_button_hash).on("click", () => {
      var param = $(target_button_hash);
      toggle_listing(param, desc, show_more_text, show_fewer_text);
    }); 

    $(".toggle-button-background").each(function () {
      toggle_listing(this, "Background", "Show", "Hide");
      $(this).on("click", () => {
        toggle_listing(this, "Background", "Show", "Hide");
      });
    });
    
  }

  // ------------------------
  function toggle_listing(
    target,
    div_description,
    show_more_text,
    show_fewer_text,
  ) {
    // How the buttons should be labelled, with
    // "More" or "Fewer" prepended.
    var target_ul = "#" + $(target).attr("data-ul");

    if ($(target).hasClass("hidden")) {
      $(target).removeClass("hidden");
      $(target_ul).removeClass("hidden");
      $(target).text(show_fewer_text + " " + div_description + " ▲");
      // Select the ID with the given prefix
      $(target_ul).show();
    } else {
      $(target).addClass("hidden");
      $(target_ul).addClass("hidden");
      $(target).text(show_more_text + " " + div_description + " ▼");
      $(target_ul).hide();
    }
  } // end toggle_listing

  /* ----- INIT CODE ------ */

  // Insert buttons everywhere!
  $(".togglable").each(add_toggle_button);

  $(".toggle-button-background").each(function () {
    toggle_listing(this, "Background", "Show", "Hide");
    $(this).on("click", () => {
      toggle_listing(this, "Background", "Show", "Hide");
    });
  });

  /* ----- WORKSHEETS PANEL ----- */

  (function() {
    var btn = document.getElementById('worksheets-btn');
    var panel = document.getElementById('worksheets-panel');
    if (!btn || !panel) return;


    function openPanel() {
      var rect = btn.getBoundingClientRect();
      panel.style.top = rect.top + 'px';
      panel.style.right = (window.innerWidth - rect.right) + 'px';
      panel.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      window.addEventListener("scroll", function () {
        closePanel();
      });
    }

    function closePanel() {
      panel.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
    }

    btn.addEventListener('click', function() {
      if (panel.hidden) { openPanel(); } else { closePanel(); }
    });

    panel.querySelectorAll('.worksheets-close').forEach(function(el) {
      el.addEventListener('click', closePanel);
    });
  }());

  // The togglable init collapses everything by default.
  // On issue pages: re-show the backgrounder on first visit; leave collapsed on return visits.
  var issueMain = document.querySelector("[data-issue-tag]");
  if (issueMain) {
    var issueTag = issueMain.getAttribute("data-issue-tag");
    var storageKey = "wrv-issue-visited-" + issueTag;
    var lastVisit = localStorage.getItem("wrv-issue-visited-" + issueTag);
    var backgrounderBtn = document.getElementById("issue-backgrounder-btn");

    if (backgrounderBtn && !lastVisit) {
      backgrounderBtn.click();
    }

    var today = new Date().toISOString().slice(0, 10);
    document.querySelectorAll(".issue-news-item").forEach(function (li) {
      var pubdate = li.getAttribute("data-pubdate");
      li.classList.add(
        lastVisit && pubdate <= lastVisit ? "issue-news-old" : "issue-news-new",
      );
    });

    localStorage.setItem(storageKey, today);
  }
});
