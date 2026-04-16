document.addEventListener("DOMContentLoaded", function() {
  var loader = document.querySelector(".map-loader[data-baseurl]");
  var status = document.getElementById("map-loader-status");

  if (!loader || !status) {
    return;
  }

  var baseUrl = loader.getAttribute("data-baseurl") || "";
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
    status.textContent = "Loading the ward map and search tools.";

    try {
      await loadScript(baseUrl + "/assets/js/leaflet.js");
      await loadScript(baseUrl + "/assets/js/leaflet-search.min.js");
      await loadScript("https://unpkg.com/leaflet-pip@1.1.0/leaflet-pip.js");
      await loadScript(baseUrl + "/assets/js/show-map.js");
      await window.WRVotesInitMap(baseUrl);
      loader.hidden = true;
    } catch (error) {
      isLoading = false;
      status.textContent = "The map could not be loaded right now.";
      console.error(error);
    }
  }

  function scheduleLoad() {
    if ("requestIdleCallback" in window) {
      window.requestIdleCallback(loadMap, { timeout: 2000 });
      return;
    }

    window.requestAnimationFrame(loadMap);
  }

  if (document.readyState === "complete") {
    scheduleLoad();
    return;
  }

  window.addEventListener("load", scheduleLoad, { once: true });
});
