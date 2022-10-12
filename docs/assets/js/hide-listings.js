/*** 
 * Helper scripts to show/hide elements of candidate lists.
 * (This was not the highest priority item...)
 */

$( document ).ready(function() {
  var WIDESCREEN = 1100;

  /* Compute a button label based upon the classes
   * in a particular ID.
   */
  function get_description( id ) { 
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
    } 

    return desc;
  } // get_description  


  function add_toggle_button ( ) { 
    var target =  $(this).attr('id');
    var classes = $(this).attr('class').split(/\s+/);

    var classes_to_add = '';
    // Ugh. Remove "togglable" from the list of 
    // classes to add to the button.
    for (var i = 0; i < classes.length; i++) { 
      if (classes[i] !== 'togglable') { 
        classes_to_add = classes_to_add + ' ' + classes[i];
      } // endif 
    } // end for

    retval = '<button data-ul="' + target + '" '
             + 'id="' + target + '-btn" '
             + 'class="toggle-button v04'
             + ' ' + target + ' ' + classes_to_add
             + '" >'
             + 'Init '
             + get_description( '#' + target )
             + '</button>';
    $(this).parent().append(retval);
  };

  function toggle_listing ( target ) { 

    // How the buttons should be labelled, with 
    // "More" or "Fewer" prepended.
    var div_description = get_description( target );
    var target_ul = "#" + $(target).attr('data-ul');

    if ($(target).hasClass('hidden')) {
      $(target).removeClass('hidden');
      $(target).text("⇧ Show Fewer " + div_description + " ⇧"); 
      // Select the ID with the given prefix
      $(target_ul).show();
    } else {
      $(target).addClass('hidden');
      $(target).text("⇩ Show More " + div_description + " ⇩");
      $(target_ul).hide();

    }
  }; // end toggle_listing

  /* ----- TOC TOGGLE ----- */

  function add_toc_toggle_button ( ) { 
    var target =  $(this).attr('id');

    retval = '<button data-toc="' + target + '" '
             + 'id="' + target + '-btn" '
             + 'class="toggle-toc" title="Toggle table of contents">'
             + 'Init'
             + '</button>';
    $(this).parent().prepend(retval);
  };


  function toggle_toc ( target_button ) { 

    var target_ul = "#toc-list";

    if ($(target_ul).hasClass('hidden')) {
      $(target_ul).removeClass('hidden');
      $(target_button).text("–");
      // Select the ID with the given prefix
      $(target_ul).slideDown();
    } else {
      $(target_ul).addClass('hidden');
      $(target_button).text("+");
      $(target_ul).slideUp();
    }
  }; // end toggle_listing

  /* ----- INIT CODE ------ */

  // Insert buttons everywhere!
  $(".togglable").each( add_toggle_button );
  $("#toc-list").each( add_toc_toggle_button );

  // Will only appear hidden in mobile mode now
  toggle_toc("#toc-list-btn");
      

  $(".toggle-toc").on("click", function (e) { 
      toggle_toc ("#" + e.target.id);
  });

  $(".toggle-button").each( function() {
    toggle_listing ("#" + this.id );
  }); 

  $(".toggle-button").on("click", function (e) { 
      toggle_listing ("#" + e.target.id );
  });

});
