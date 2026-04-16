document.addEventListener("DOMContentLoaded", function() {
  var button = document.getElementById("load-map-button");
  var status = document.getElementById("map-loader-status");

  if (!button || !status) {
    return;
  }

  var baseUrl = button.getAttribute("data-baseurl") || "";
  var isLoading = false;

  function loadScript(src) {
    return new Promise(function(resolve, reject) {
      var script = document.createElement("script");
      script.src = src;
      script.defer = true;
      script.onload = resolve;
      script.onerror = function() {
        reject(new Error("Failed to load " + src));
      };
      document.body.appendChild(script);
    });
  }

  async function loadMap() {
    if (isLoading) {
      return;
    }

    isLoading = true;
    button.disabled = true;
    button.textContent = "Loading map...";
    status.textContent = "Loading the ward map and search tools.";

    try {
      await loadScript(baseUrl + "/assets/js/leaflet.js");
      await loadScript(baseUrl + "/assets/js/leaflet-search.min.js");
      await loadScript("https://unpkg.com/leaflet-pip@1.1.0/leaflet-pip.js");
      await loadScript(baseUrl + "/assets/js/show-map.js");
      await window.WRVotesInitMap(baseUrl);
      button.hidden = true;
      status.textContent = "The interactive map is ready.";
    } catch (error) {
      isLoading = false;
      button.disabled = false;
      button.textContent = "Try loading the map again";
      status.textContent = "The map could not be loaded right now.";
      console.error(error);
    }
  }

  button.addEventListener("click", loadMap);
});
