/*** 
 * Helper scripts to show/hide elements of candidate lists.
 * (This was not the highest priority item...)
 */

$( document ).ready(function() {

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
    } 

    return desc;
  } // get_description  

  function add_button_to_parent ( ) { 
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

    retval = '<button name="foo" '
             + 'id="' + target + '-btn" '
             + 'class="toggle-button test'
             + ' ' + classes_to_add 
             + '">'
             + 'Init '
             + get_description( '#' + target )
             + '</button>';
    $(this).parent().prepend(retval);
  };

  function toggle_listing ( target ) { 

    // How the buttons should be labelled, with 
    // "More" or "Fewer" prepended.
    var div_description = get_description( target );

    if ($(target).hasClass('hidden')) {
      $(target).removeClass('hidden');
      $(target).text("Fewer " + div_description); 
      $(target + " ~ .togglable").show();
    } else {
      $(target).addClass('hidden');
      $(target).text("More " + div_description);
      $(target + " ~ .togglable").hide();
    }
  }; // end toggle_listing

  /* ----- INIT CODE ------ */

  // Insert buttons everywhere!
  $(".togglable").each( add_button_to_parent );

  $(".toggle-button").each( function() {
    toggle_listing ("#" + this.id );
  }); 

  $(".toggle-button").on("click", function (e) { 
      toggle_listing ("#" + e.target.id );
  });

});
