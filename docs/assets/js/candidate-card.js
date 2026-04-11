$(document).ready(function () {
    $("h3.no-website").on("click", (e) => {
        tooltip_id = $(e.target).attr('aria-describedby');
        tooltip_e = $("#" + tooltip_id)
        if (tooltip_e.hasClass("hidden")) {
            tooltip_e.removeClass("hidden");
            setTimeout(() => {
                tooltip_e.addClass("hidden");
            }, 3000);
        }
    });
});