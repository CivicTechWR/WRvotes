function parseFavourites() {
    var favouritesRaw = localStorage.getItem("wrv-favourited");
    return favouritesRaw ? JSON.parse(favouritesRaw) : [];
}

function saveFavourite(candidate) {
    var favourites = parseFavourites();
    if (!favourites.includes(candidate)) {
        favourites.push(candidate);
        localStorage.setItem('wrv-favourited', JSON.stringify(favourites));
    }
}

function removeFavourite(candidate) {
    var favourites = parseFavourites();
    favourites = favourites.filter(x => x != candidate);
    localStorage.setItem('wrv-favourited', JSON.stringify(favourites));
}

function saveNote(candidate, content) {
    localStorage.setItem('wrv-note-' + candidate, content);
}

function loadNote(candidate) {
    return localStorage.getItem('wrv-note-' + candidate) || '';
}

$(document).ready(function () {
    $(".auto-resize-textarea[data-candidate-id]").each(function () {
        var saved = loadNote($(this).attr("data-candidate-id"));
        if (saved) {
            $(this).html(saved);
        }
    });

    var debounce;
    $(".auto-resize-textarea[data-candidate-id]").on("input", function () {
        var el = $(this);
        clearTimeout(debounce);
        debounce = setTimeout(function () {
            saveNote(el.attr("data-candidate-id"), el.html());
        }, 300);
    });

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

    $(".favourite-btn").on("click", function () {
        var candidate = $(this).attr("data-candidate-id");
        $(this).toggleClass("favourited");
        var icon = $(this).find("i");
        if ($(this).hasClass("favourited")) {
            icon.removeClass("fa-regular").addClass("fa-solid");
            saveFavourite(candidate);
        } else {
            icon.removeClass("fa-solid").addClass("fa-regular");
            removeFavourite(candidate);
        }
    });

    for (var candidate of parseFavourites()) {
        var btn = $(".favourite-btn[data-candidate-id='" + candidate + "']");
        if (btn.length) {
            btn.addClass("favourited");
            btn.find("i").removeClass("fa-regular").addClass("fa-solid");
        }
    }

    $("#worksheet-no-js-warning").hide();
});
