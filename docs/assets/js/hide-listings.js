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
    var desc = "Results";

    if ($(id).hasClass("candidate-list")) {
      desc = "This Listing";
    } else if ($(id).hasClass("event-list")) {
      desc = "Events";
    } else if ($(id).hasClass("survey-list")) {
      desc = "Questionnaires";
    } else if ($(id).hasClass("news-list")) {
      desc = "News Items";
    } else if ($(id).hasClass("blogs-list")) {
      desc = "Opinions";
    } else if ($(id).hasClass("recordings-list")) {
      desc = "Recordings";
    } else if ($(id).hasClass("background")) {
      desc = "Background";
    }

    return desc;
  } // get_description

  // ------------------------
  function add_toggle_button() {
    var target = $(this).attr("id");
    var classes = $(this).attr("class").split(/\s+/);
    var toggle_button_cls = "toggle-button";
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
      ` id="${target}-btn"` +
      ` class="${toggle_button_cls} v04 ${target} ${classes_to_add}" >` +
      `Init ${get_description("#" + target)}` +
      "</button>";
    $(this).parent().append(retval);
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
    var target_ul = target.attr("data-ul");

    if ($(target).hasClass("hidden")) {
      $(target).removeClass("hidden");
      $(target).text(show_fewer_text + " " + div_description + " ▲");
      // Select the ID with the given prefix
      $(target_ul).show();
    } else {
      $(target).addClass("hidden");
      $(target).text(show_more_text + " " + div_description + " ▼");
      $(target_ul).hide();
    }
  } // end toggle_listing

  /* ----- TOC TOGGLE ----- */

  // ------------------------
  function add_ul_toggle_button(target, classname, title, inittext) {
    console.log("add_ul_target_button: Target is " + target);

    retval =
      '<button data-toc="' +
      target +
      '" ' +
      'id="' +
      target +
      '-btn" ' +
      'class="' +
      classname +
      '" title="' +
      title +
      '">' +
      inittext +
      "</button>";
    $("#" + target)
      .parent()
      .prepend(retval);
  }

  // ------------------------
  function add_toc_toggle_button() {
    var target = $(this).attr("id");
    add_ul_toggle_button(target, "toggle-toc", "Toggle table of contents", "–");
  }

  // ------------------------
  function add_menu_toggle_button() {
    var target = $(this).attr("id");
    add_ul_toggle_button(
      target,
      "toggle-menu",
      "toggle main menu",
      '<i class="fas fa-bars"></i>',
    );
  }

  // ------------------------
  function toggle_main_menu() {
    var target_ul = "#main-menu-ul";

    if ($(target_ul).hasClass("hidden")) {
      $(target_ul).removeClass("hidden");
      $(target_ul).slideDown();
    } else {
      $(target_ul).addClass("hidden");
      $(target_ul).slideUp();
    }
  }

  // ------------------------
  function toggle_toc(target_button) {
    var target_ul = "#toc-list";

    if ($(target_ul).hasClass("hidden")) {
      $(target_ul).removeClass("hidden");
      $(target_button).text("–");
      // Select the ID with the given prefix
      $(target_ul).slideDown();
    } else {
      $(target_ul).addClass("hidden");
      $(target_button).text("+");
      $(target_ul).slideUp();
    }
  } // end toggle_toc

  /* ----- INIT CODE ------ */

  // Insert buttons everywhere!
  $("#toc-list").each(add_toc_toggle_button);
  $("#main-menu-ul").each(add_menu_toggle_button);
  $(".togglable").each(add_toggle_button);

  $(".toggle-toc").on("click", function (e) {
    toggle_toc("#" + e.target.id);
  });

  $(".toggle-menu").on("click", function (e) {
    toggle_main_menu("#" + e.target.id);
  });

  $(".toggle-button").each(function () {
    var div_description = get_description(`#${this.id}`);
    toggle_listing(this, div_description, "Show More", "Show Fewer");
    $(this).on("click", () => {
      toggle_listing(this, div_description, "Show More", "Show Fewer");
    });
  });

  $(".toggle-button-background").each(function () {
    toggle_listing(this, "Background", "Show", "Hide");
    $(this).on("click", () => {
      toggle_listing(this, "Background", "Show", "Hide");
    });
  });

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
