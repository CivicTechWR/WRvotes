var WRV_FAVOURITE_KEY = "wrv-favourited";
var WRV_NOTE_PREFIX = "wrv-note-";

function parseFavourites() {
    var favouritesRaw = localStorage.getItem(WRV_FAVOURITE_KEY);
    return favouritesRaw ? JSON.parse(favouritesRaw) : [];
}

function saveFavourite(candidate) {
    var favourites = parseFavourites();
    if (!favourites.includes(candidate)) {
        favourites.push(candidate);
        localStorage.setItem(WRV_FAVOURITE_KEY, JSON.stringify(favourites));
    }
}

function removeFavourite(candidate) {
    var favourites = parseFavourites();
    favourites = favourites.filter(x => x != candidate);
    localStorage.setItem(WRV_FAVOURITE_KEY, JSON.stringify(favourites));
}

function updateFavourites() {
    var favouritedCandidates = parseFavourites();
    $(".favourite-btn[data-candidate-id]").each(function () {
        var btn = $(this);
        if (favouritedCandidates.includes(btn.attr("data-candidate-id"))) {
            btn.addClass("favourited");
            btn.find("i").removeClass("fa-regular").addClass("fa-solid");
        } else {
            btn.removeClass("favourited");
            btn.find("i").removeClass("fa-solid").addClass("fa-regular");
        }
    });
}
 
function saveNote(candidate, content) {
    localStorage.setItem(WRV_NOTE_PREFIX + candidate, content);
}

function loadNote(candidate) {
    return localStorage.getItem(WRV_NOTE_PREFIX + candidate) || '';
}

function updateNotes() {
    $(".auto-resize-textarea[data-candidate-id]").each(function () {
        var saved = loadNote($(this).attr("data-candidate-id"));
        if (saved) {
            $(this).html(saved);
        }
    });
}

$(document).ready(function () {
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

    $(".notes-btn").on("click", function () {
        var candidate = $(this).attr("data-candidate-id");
        $(this).toggleClass("opened");
        var icon = $(this).find("i");
        var notes = $(`.auto-resize-textarea[data-candidate-id='${candidate}']`);
        if (notes) { 
            if ($(this).hasClass("opened")) {
                icon.removeClass("fa-regular").addClass("fa-solid");
                notes.closest(".notes-container").addClass("open");
            } else {
                icon.removeClass("fa-solid").addClass("fa-regular");
                notes.closest(".notes-container").removeClass("open");
            }
        }
    });

    updateNotes();
    updateFavourites();

    window.addEventListener("storage", (event) => {
        if (event.key === WRV_FAVOURITE_KEY) {
            updateFavourites();
        } else if (event.key.startsWith(WRV_NOTE_PREFIX)) {
            updateNotes();
        }
    });

    $("#worksheet-no-js-warning").hide();
});
