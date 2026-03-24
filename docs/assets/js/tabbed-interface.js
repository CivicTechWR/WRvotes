/*** 
 * Implement tabbed interface using Javascript 
 */

$( document ).ready(function() {

  function select_tab (evt) { 
    var target = evt.target
    // console.log("Target is " + JSON.stringify(target));
    console.log("Href is " + JSON.stringify(target.href));

    
    // var target_href = target.split('#').pop();
    // console.log("Target href is " + target_href);

    var anchor = target.href.split('#').pop();
    console.log("Anchor is " + anchor);

    // STOP from actually visiting the link! Yikes!
    evt.preventDefault();

    // Change URL to set new target. Now CSS should work?
    // NOPE. This does NOT update the target!
    // https://www.codegenes.net/blog/how-to-prevent-jump-on-an-anchor-click/#51-updating-the-url-hash-without-jumping
    history.pushState({}, '', '#' + anchor);

  }; // end select_tab



  /* ---- INIT CODE --- */
  $("[role='tab']").on("click", function (e) { 
      select_tab ( e );
  });

});
