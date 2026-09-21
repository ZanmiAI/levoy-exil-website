/* ============================================================
   Zanmi Studio — Artist Site Template · main.js
   - Mobile navigation toggle
   - Gallery availability filtering
   - Click-to-play video facades (custom sections)
   - Studio products showcase auto-hide (empty => hidden)
   ============================================================ */
(function () {
  "use strict";

  /* ---- Mobile nav ---- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* ---- Gallery filters ---- */
  var filterBtns = document.querySelectorAll(".filter-btn");
  var cards = document.querySelectorAll("[data-availability]");
  var countEl = document.querySelector(".gallery-count");
  function applyFilter(value) {
    var shown = 0;
    cards.forEach(function (card) {
      var show = value === "all" || card.getAttribute("data-availability") === value;
      card.style.display = show ? "" : "none";
      if (show) shown++;
    });
    if (countEl) {
      countEl.textContent = shown + (shown === 1 ? " artwork" : " artworks");
    }
    filterBtns.forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.getAttribute("data-filter") === value ? "true" : "false");
    });
  }
  if (filterBtns.length && cards.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        applyFilter(btn.getAttribute("data-filter"));
      });
    });
  }

  /* ---- Artwork gallery lightbox ----
     Clicking a "More photos" thumbnail opens the full uncropped photo.
     Closes on click, the X button, or the Escape key. */
  document.querySelectorAll(".artwork-gallery-grid img").forEach(function (img) {
    img.addEventListener("click", function () {
      var overlay = document.createElement("div");
      overlay.className = "lightbox";
      overlay.setAttribute("role", "dialog");
      overlay.setAttribute("aria-label", "Photo enlarged");
      var full = document.createElement("img");
      full.src = img.currentSrc || img.src;
      full.alt = img.alt;
      var close = document.createElement("button");
      close.className = "lightbox-close";
      close.setAttribute("aria-label", "Close");
      close.innerHTML = "&times;";
      overlay.appendChild(full);
      overlay.appendChild(close);
      function dismiss() { overlay.remove(); document.removeEventListener("keydown", onKey); }
      function onKey(e) { if (e.key === "Escape") dismiss(); }
      overlay.addEventListener("click", dismiss);
      document.addEventListener("keydown", onKey);
      document.body.appendChild(overlay);
    });
  });

  /* ---- Click-to-play video facades (custom sections) ----
     The thumbnail image swaps in a privacy-enhanced YouTube embed
     only after the visitor taps play. */
  document.querySelectorAll(".video-facade").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var id = btn.getAttribute("data-youtube-id");
      if (!id) return;
      var frame = document.createElement("iframe");
      frame.src = "https://www.youtube-nocookie.com/embed/" +
        encodeURIComponent(id) + "?autoplay=1&rel=0";
      frame.title = btn.getAttribute("aria-label") || "Video";
      frame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      frame.allowFullscreen = true;
      frame.className = "video-frame";
      btn.replaceWith(frame);
    });
  });

  /* ---- Studio products showcase: hide when empty ----
     The static generator omits this section when the product list
     is empty, but this guard keeps it hidden even if the section
     markup exists with zero product cards (e.g. hand-edited HTML). */
  document.querySelectorAll("[data-products-showcase]").forEach(function (section) {
    if (!section.querySelector(".product-card")) {
      section.hidden = true;
      section.style.display = "none";
    }
  });
})();
