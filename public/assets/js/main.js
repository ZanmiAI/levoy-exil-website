/* ============================================================
   Zanmi Studio — Artist Site Template · main.js
   - Mobile navigation toggle
   - Gallery availability filtering
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
