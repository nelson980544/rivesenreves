/* ==========================================================================
   RivesEnRêves — scripts communs (léger, sans dépendance)
   - menu mobile
   - apparition des blocs au défilement
   - filtres (références, blog)
   Le site reste entièrement lisible sans JavaScript.
   ========================================================================== */
(function () {
  "use strict";

  /* Menu mobile ---------------------------------------------------------- */
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("menu-principal");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
        toggle.focus();
      }
    });
  }

  /* Apparition au défilement --------------------------------------------- */
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* Filtres par univers (pages Références et Blog) ----------------------- */
  document.querySelectorAll("[data-filter-group]").forEach(function (group) {
    var target = document.querySelector(group.getAttribute("data-filter-target"));
    if (!target) return;
    var buttons = group.querySelectorAll("button[data-filter]");
    function apply(value) {
      buttons.forEach(function (b) {
        b.setAttribute("aria-pressed", String(b.getAttribute("data-filter") === value));
      });
      target.querySelectorAll("[data-univers]").forEach(function (card) {
        var list = card.getAttribute("data-univers").split(" ");
        card.hidden = value !== "tous" && list.indexOf(value) === -1;
      });
    }
    buttons.forEach(function (b) {
      b.addEventListener("click", function () { apply(b.getAttribute("data-filter")); });
    });
    group.hidden = false;
    // Filtre présélectionné par l'URL : references/?univers=plaisanciers
    var initial = new URLSearchParams(window.location.search).get("univers");
    apply(initial && group.querySelector('[data-filter="' + initial + '"]') ? initial : "tous");
  });
})();
