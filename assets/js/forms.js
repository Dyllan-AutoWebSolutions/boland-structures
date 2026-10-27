/* Boland Structures — form handling (contact.html, quote.html)
 *
 * Sending: this is a static site, so forms run in demo mode by default and
 * show the success screen without sending anything. To make them live, add
 * a form endpoint to the <form> tag, for example a Formspree or Netlify Forms URL:
 *   <form ... data-endpoint="https://formspree.io/f/xxxxxxx">
 * The form data is then POSTed there as multipart/form-data.
 */
(function () {
  "use strict";

  /* ---------- Validation ---------- */
  function containerOf(el) {
    return el.closest(".fieldset[data-group]") || el.closest(".field");
  }

  function setState(container, el, valid) {
    if (!container) return;
    container.classList.toggle("is-invalid", !valid);
    var check = container.querySelector(".check");
    if (check) check.classList.toggle("is-invalid", !valid);
    if (el) el.setAttribute("aria-invalid", String(!valid));
  }

  function validateGroup(fieldset) {
    var radios = fieldset.querySelectorAll("input[type=radio]");
    var valid = Array.prototype.some.call(radios, function (r) { return r.checked; });
    setState(fieldset, null, valid);
    radios.forEach(function (r) { r.setAttribute("aria-invalid", String(!valid)); });
    return valid ? null : radios[0];
  }

  function validateInput(el) {
    // minlength alone only fires after typing and counts spaces, so check the trimmed length too
    var len = el.value ? el.value.trim().length : 0;
    var tooShort = el.minLength > 0 && len > 0 && len < el.minLength;
    var valid = el.checkValidity() && !tooShort && !(el.required && el.type !== "checkbox" && len === 0);
    setState(containerOf(el), el, valid);
    return valid ? null : el;
  }

  // Validates everything inside `scope`; returns the first invalid control (or null)
  function validateScope(scope) {
    var firstBad = null;
    scope.querySelectorAll("input:not([type=radio]), select, textarea").forEach(function (el) {
      var bad = validateInput(el);
      if (bad && !firstBad) firstBad = bad;
    });
    scope.querySelectorAll(".fieldset[data-group]").forEach(function (fs) {
      var bad = validateGroup(fs);
      if (bad && !firstBad) firstBad = bad;
    });
    return firstBad;
  }

  function wireLiveValidation(form) {
    form.addEventListener("blur", function (e) {
      var el = e.target;
      if (el.matches("input:not([type=radio]):not([type=checkbox]), select, textarea") && el.value) validateInput(el);
    }, true);
    form.addEventListener("input", recheck);
    form.addEventListener("change", recheck);
    function recheck(e) {
      var el = e.target;
      var container = containerOf(el);
      if (!container || !container.classList.contains("is-invalid")) return;
      if (el.type === "radio") validateGroup(container); else validateInput(el);
    }
  }

  /* ---------- Submit (demo or live endpoint) ---------- */
  function send(form) {
    var endpoint = form.getAttribute("data-endpoint");
    if (!endpoint) {
      return new Promise(function (resolve) { setTimeout(resolve, 900); });
    }
    return fetch(endpoint, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
      .then(function (r) { if (!r.ok) throw new Error("Send failed"); });
  }

  function reference(prefix) {
    var d = new Date();
    var n = Math.floor(1000 + Math.random() * 9000);
    return prefix + "-" + d.getFullYear() + String(d.getMonth() + 1).padStart(2, "0") + "-" + n;
  }

  function showSuccess(form, prefix) {
    var card = form.closest(".form-card");
    var name = (form.elements.name && form.elements.name.value.trim().split(" ")[0]) || "";
    card.querySelector("[data-form-body]").hidden = true;
    var success = card.querySelector("[data-form-success]");
    success.querySelector("[data-success-name]").textContent = name;
    success.querySelector("[data-success-ref]").textContent = "Reference " + reference(prefix);
    success.hidden = false;
    scrollToCard(card);
    success.focus({ preventScroll: true });
  }

  function scrollToCard(card) {
    var header = document.querySelector(".header");
    var offset = (header ? header.offsetHeight : 0) + 16;
    var top = card.getBoundingClientRect().top + window.scrollY - offset;
    if (top < window.scrollY) window.scrollTo({ top: top, behavior: "smooth" });
  }

  function handleSubmit(form, prefix, beforeSend) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (beforeSend && beforeSend() === false) return;
      var bad = validateScope(form);
      if (bad) { bad.focus(); return; }
      var btn = form.querySelector("[type=submit]");
      var label = btn.innerHTML;
      btn.disabled = true;
      btn.textContent = "Sending…";
      send(form).then(function () {
        showSuccess(form, prefix);
      }).catch(function () {
        btn.disabled = false;
        btn.innerHTML = label;
        alert("Sorry, your message didn't send. Please call us on +27 23 347 0000.");
      });
    });
  }

  /* ---------- Contact form ---------- */
  var contact = document.querySelector("[data-form=contact]");
  if (contact) {
    wireLiveValidation(contact);
    handleSubmit(contact, "BS-C");
  }

  /* ---------- Quote form (multi-step) ---------- */
  var quote = document.querySelector("[data-form=quote]");
  if (quote) {
    var steps = quote.querySelectorAll("[data-step]");
    var stepperItems = document.querySelectorAll(".stepper li");
    var prevBtn = quote.querySelector("[data-prev]");
    var nextBtn = quote.querySelector("[data-next]");
    var submitBtn = quote.querySelector("[data-submit]");
    var card = quote.closest(".form-card");
    var current = 1;
    var total = steps.length;

    var LABELS = [
      ["service", "Service"], ["sector", "Who it's for"], ["location", "Location"], ["size", "Size"],
      ["budget", "Budget"], ["start", "Start"], ["plans", "Plans"], ["description", "Project"],
      ["name", "Name"], ["phone", "Phone"], ["email", "Email"], ["contact_method", "Contact by"]
    ];

    function buildReview() {
      var data = new FormData(quote);
      var dl = quote.querySelector("[data-review]");
      dl.innerHTML = "";
      LABELS.forEach(function (pair) {
        var value = data.get(pair[0]);
        if (pair[0] === "service" && value) value = value.charAt(0).toUpperCase() + value.slice(1);
        var row = document.createElement("div");
        var dt = document.createElement("dt");
        var dd = document.createElement("dd");
        dt.textContent = pair[1];
        dd.textContent = value || "Not given";
        row.appendChild(dt);
        row.appendChild(dd);
        dl.appendChild(row);
      });
    }

    function show(n, focus) {
      current = n;
      steps.forEach(function (s) { s.hidden = Number(s.dataset.step) !== n; });
      stepperItems.forEach(function (li, i) {
        li.classList.toggle("is-current", i + 1 === n);
        li.classList.toggle("is-done", i + 1 < n);
      });
      prevBtn.hidden = n === 1;
      nextBtn.hidden = n === total;
      submitBtn.hidden = n !== total;
      nextBtn.firstChild.textContent = n === total - 1 ? "Review request " : "Next step ";
      if (n === total) buildReview();
      if (focus) {
        scrollToCard(card);
        steps[n - 1].querySelector(".form-step__title").focus({ preventScroll: true });
      }
    }

    function next() {
      if (current >= total) return;
      var bad = validateScope(steps[current - 1]);
      if (bad) { bad.focus(); return; }
      show(current + 1, true);
    }

    nextBtn.addEventListener("click", next);
    prevBtn.addEventListener("click", function () { show(current - 1, true); });

    wireLiveValidation(quote);
    // Enter inside a field moves forward instead of submitting early
    handleSubmit(quote, "BS-Q", function () {
      if (current < total) { next(); return false; }
    });

    // Pre-select the service when arriving from a service page (?service=construction)
    var pre = new URLSearchParams(window.location.search).get("service");
    if (pre) {
      var radio = quote.querySelector('input[name=service][value="' + pre.replace(/[^a-z ]/gi, "") + '"]');
      if (radio) radio.checked = true;
    }
    show(1, false);
  }

  /* ---------- Click-to-load map ---------- */
  var mapBtn = document.querySelector("[data-map-load]");
  if (mapBtn) {
    mapBtn.addEventListener("click", function () {
      var map = mapBtn.closest("[data-map]");
      var iframe = document.createElement("iframe");
      iframe.src = "https://www.google.com/maps?q=18+Durban+Street,+Worcester,+6850&output=embed";
      iframe.title = "Map showing Boland Structures at 18 Durban Street, Worcester";
      iframe.loading = "lazy";
      iframe.referrerPolicy = "no-referrer-when-downgrade";
      map.querySelector(".map__placeholder").remove();
      map.appendChild(iframe);
    });
  }
})();
