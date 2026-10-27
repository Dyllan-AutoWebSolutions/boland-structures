/* Boland Structures — site interactions */
(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.remove("no-js");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Header shadow on scroll ---------- */
  var header = document.querySelector(".header");
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile nav ---------- */
  var burger = document.querySelector(".burger");
  var mobileNav = document.getElementById("mobile-nav");
  function setNav(open) {
    document.body.classList.toggle("nav-open", open);
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }
  if (burger && mobileNav) {
    burger.addEventListener("click", function () {
      setNav(!document.body.classList.contains("nav-open"));
    });
    mobileNav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setNav(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
        setNav(false);
        burger.focus();
      }
    });
    window.matchMedia("(min-width: 64em)").addEventListener("change", function (mq) {
      if (mq.matches) setNav(false);
    });
  }

  /* ---------- Hero slider ---------- */
  var hero = document.querySelector("[data-slider]");
  if (hero) {
    var slides = hero.querySelectorAll(".hero__slide");
    var dotsWrap = hero.querySelector(".hero__dots");
    var current = 0;
    var timer = null;
    var DELAY = 5000;

    slides.forEach(function (_, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", "Show slide " + (i + 1));
      b.addEventListener("click", function () { go(i); restart(); });
      dotsWrap.appendChild(b);
    });
    var dots = dotsWrap.querySelectorAll("button");

    function go(n) {
      slides[current].classList.remove("is-active");
      slides[current].setAttribute("aria-hidden", "true");
      current = (n + slides.length) % slides.length;
      slides[current].classList.add("is-active");
      slides[current].removeAttribute("aria-hidden");
      dots.forEach(function (d, i) { d.setAttribute("aria-current", String(i === current)); });
    }
    function restart() {
      clearInterval(timer);
      if (!reduceMotion) timer = setInterval(function () { go(current + 1); }, DELAY);
    }

    hero.querySelector(".hero__arrow--prev").addEventListener("click", function () { go(current - 1); restart(); });
    hero.querySelector(".hero__arrow--next").addEventListener("click", function () { go(current + 1); restart(); });
    hero.addEventListener("mouseenter", function () { clearInterval(timer); });
    hero.addEventListener("mouseleave", restart);
    hero.addEventListener("focusin", function () { clearInterval(timer); });

    // Swipe on touch devices
    var startX = null;
    hero.addEventListener("touchstart", function (e) { startX = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener("touchend", function (e) {
      if (startX === null) return;
      var dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 50) { go(current + (dx < 0 ? 1 : -1)); restart(); }
      startX = null;
    });

    document.addEventListener("visibilitychange", function () {
      document.hidden ? clearInterval(timer) : restart();
    });

    go(0);
    restart();
  }

  /* ---------- About tabs ---------- */
  document.querySelectorAll("[role='tablist']").forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll("[role='tab']"));
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
    }
    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { select(tab); });
      tab.addEventListener("keydown", function (e) {
        var next = null;
        if (e.key === "ArrowRight") next = tabs[(i + 1) % tabs.length];
        if (e.key === "ArrowLeft") next = tabs[(i - 1 + tabs.length) % tabs.length];
        if (next) { e.preventDefault(); select(next); next.focus(); }
      });
    });
  });

  /* ---------- Count-up stats ---------- */
  function countUp(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (reduceMotion) { el.textContent = target; return; }
    var start = null;
    var dur = 1600;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ---------- Reveal on scroll ---------- */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        entry.target.querySelectorAll("[data-count]").forEach(countUp);
        io.unobserve(entry.target);
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---------- Sub-nav: highlight the section in view ---------- */
  var subnav = document.querySelector(".subnav");
  var spied = document.querySelectorAll("[data-spy]");
  if (subnav && spied.length && "IntersectionObserver" in window) {
    var links = subnav.querySelectorAll("a");
    var list = subnav.querySelector(".subnav__list");
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) {
          var on = a.getAttribute("href") === "#" + entry.target.id;
          a.classList.toggle("is-active", on);
          if (on) {
            a.setAttribute("aria-current", "true");
            // Keep the active chip visible on narrow screens without moving the page
            list.scrollTo({ left: a.offsetLeft - 16, behavior: reduceMotion ? "auto" : "smooth" });
          } else {
            a.removeAttribute("aria-current");
          }
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    spied.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- Project filters ---------- */
  var filterBar = document.querySelector("[data-filters]");
  if (filterBar) {
    var buttons = filterBar.querySelectorAll("[data-filter]");
    var cards = document.querySelectorAll("[data-sector]");
    var status = document.querySelector(".filter-status");

    function applyFilter(value, push) {
      var shown = 0;
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.filter === value)); });
      cards.forEach(function (card) {
        var match = value === "all" || card.dataset.sector === value;
        if (match) {
          shown++;
          if (card.hidden) {
            card.hidden = false;
            card.classList.remove("is-entering");
            void card.offsetWidth; // restart the entry animation
            card.classList.add("is-entering");
          }
        } else {
          card.hidden = true;
        }
      });
      if (status) {
        status.textContent = "Showing " + shown + " " + (shown === 1 ? "project" : "projects") +
          (value === "all" ? "" : " in " + value.toLowerCase());
      }
      if (push) {
        var url = new URL(window.location);
        if (value === "all") url.searchParams.delete("sector"); else url.searchParams.set("sector", value);
        history.replaceState(null, "", url);
      }
    }

    buttons.forEach(function (b) {
      b.addEventListener("click", function () { applyFilter(b.dataset.filter, true); });
    });
    var initial = new URLSearchParams(window.location.search).get("sector");
    var valid = Array.prototype.some.call(buttons, function (b) { return b.dataset.filter === initial; });
    applyFilter(valid ? initial : "all", false);
  }

  /* ---------- Gallery lightbox ---------- */
  var lightbox = document.getElementById("lightbox");
  var galleryItems = document.querySelectorAll("[data-lightbox]");
  if (lightbox && galleryItems.length && typeof lightbox.showModal === "function") {
    var lbImg = lightbox.querySelector("img");
    var lbCaption = lightbox.querySelector(".lightbox__caption");
    var lbCount = lightbox.querySelector(".lightbox__count");
    var lbIndex = 0;
    var lbOpener = null;

    function show(i) {
      lbIndex = (i + galleryItems.length) % galleryItems.length;
      var item = galleryItems[lbIndex];
      var thumb = item.querySelector("img");
      lbImg.src = item.getAttribute("href");
      lbImg.alt = thumb.alt;
      lbCaption.textContent = thumb.alt;
      lbCount.textContent = (lbIndex + 1) + " / " + galleryItems.length;
    }

    galleryItems.forEach(function (item, i) {
      item.addEventListener("click", function (e) {
        e.preventDefault();
        lbOpener = item;
        show(i);
        lightbox.showModal();
      });
    });
    lightbox.querySelector(".lightbox__prev").addEventListener("click", function () { show(lbIndex - 1); });
    lightbox.querySelector(".lightbox__next").addEventListener("click", function () { show(lbIndex + 1); });
    lightbox.querySelector(".lightbox__close").addEventListener("click", function () { lightbox.close(); });
    lightbox.addEventListener("click", function (e) { if (e.target === lightbox) lightbox.close(); });
    lightbox.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") show(lbIndex + 1);
      if (e.key === "ArrowLeft") show(lbIndex - 1);
    });
    lightbox.addEventListener("close", function () {
      // Defer so the dialog's own focus restore doesn't override ours
      if (lbOpener) setTimeout(function () { lbOpener.focus(); }, 0);
    });

    var lbStartX = null;
    lightbox.addEventListener("touchstart", function (e) { lbStartX = e.touches[0].clientX; }, { passive: true });
    lightbox.addEventListener("touchend", function (e) {
      if (lbStartX === null) return;
      var dx = e.changedTouches[0].clientX - lbStartX;
      if (Math.abs(dx) > 50) show(lbIndex + (dx < 0 ? 1 : -1));
      lbStartX = null;
    });
  }

  /* ---------- Footer year ---------- */
  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
