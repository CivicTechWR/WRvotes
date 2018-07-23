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

  //$.fn.add_button_to_parent = function () { 
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
             + 'Hide '
             + get_description( '#' + target )
             + '</button>';
    $(this).parent().prepend(retval);
  };

  /* ----- INIT CODE ------ */

  // Insert buttons everywhere!
  $(".togglable").each( add_button_to_parent );

  $(".toggle-button").on("click", function(e) {
    var target = "#" + e.target.id;

    // How the buttons should be labelled, with 
    // "show" or "hide" prepended.
    var div_description = get_description( target );

    $("#debug-messages").html("<p>target is: " + target
                              + "</p>")
    if ($(target).hasClass('hidden')) {
      $(target).removeClass('hidden');
      $(target).text("Hide " + div_description); 
      $(target + " ~ .togglable").show();
    } else {
      $(target).addClass('hidden');
      $(target).text("Show " + div_description);
      $(target + " ~ .togglable").hide();
    }
  });

});
