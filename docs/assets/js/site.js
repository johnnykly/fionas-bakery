// Fiona's Bakery: small progressive enhancements. The site works without JS.
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  // Header border once the page has scrolled (observer on a sentinel, no scroll listener).
  const header = document.querySelector(".site-header");
  const sentinel = document.getElementById("top");
  if (header && sentinel && "IntersectionObserver" in window) {
    new IntersectionObserver(([entry]) => {
      header.classList.toggle("is-scrolled", !entry.isIntersecting);
    }).observe(sentinel);
  }

  // Mobile menu
  const toggle = document.querySelector(".menu-toggle");
  if (toggle) {
    const setOpen = (open) => {
      document.body.classList.toggle("menu-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Stäng meny" : "Öppna meny");
    };
    toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") setOpen(false); });
    document.querySelectorAll(".nav a").forEach((a) => a.addEventListener("click", () => setOpen(false)));
  }

  // Reveal on scroll
  const revealables = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { entry.target.classList.add("is-in"); io.unobserve(entry.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    revealables.forEach((el) => io.observe(el));
  } else {
    revealables.forEach((el) => el.classList.add("is-in"));
  }

  // Order form
  const form = document.getElementById("order-form");
  if (!form) return;

  const $ = (name) => form.elements.namedItem(name);
  const occasion = $("tillfalle");
  const date = $("datum");
  const dateWarn = document.getElementById("datum-warn");
  const addressWrap = document.getElementById("adress-wrap");
  const status = document.getElementById("form-status");
  const submit = form.querySelector('button[type="submit"]');

  // Pre-select occasion from ?tillfalle=
  const fromQuery = new URLSearchParams(location.search).get("tillfalle");
  if (fromQuery && occasion) {
    const match = Array.from(occasion.options).find((o) => o.value === fromQuery);
    if (match) occasion.value = fromQuery;
  }

  // Earliest selectable date: today
  const today = new Date();
  const iso = (d) => new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  if (date) date.min = iso(today);

  const updateDateWarning = () => {
    if (!date || !date.value || !dateWarn) { if (dateWarn) dateWarn.textContent = ""; return; }
    const days = Math.round((new Date(date.value + "T12:00") - today) / 86400000);
    const isWedding = occasion && occasion.value === "brollop";
    const needed = isWedding ? 30 : 7;
    dateWarn.textContent = days >= 0 && days < needed
      ? (isWedding
        ? "Tårtor med sockerblommor behöver helst en månad. Skicka gärna ändå, så ser jag vad jag hinner."
        : "Det är kort om tid. Skicka gärna ändå, ibland går det att lösa.")
      : "";
  };
  date && date.addEventListener("change", updateDateWarning);
  occasion && occasion.addEventListener("change", updateDateWarning);

  const updateDelivery = () => {
    const delivery = form.querySelector('input[name="leverans"]:checked');
    const on = delivery && delivery.value === "Leverans";
    addressWrap.hidden = !on;
    $("adress").required = on;
  };
  form.querySelectorAll('input[name="leverans"]').forEach((r) => r.addEventListener("change", updateDelivery));
  updateDelivery();

  const messages = {
    valueMissing: "Fyll i det här fältet.",
    typeMismatch: { email: "Skriv en giltig e-postadress, till exempel namn@exempel.se.", url: "Skriv en hel länk som börjar med https://" },
    rangeUnderflow: "Ange minst 1.",
    patternMismatch: "Skriv ett telefonnummer med siffror, till exempel 070-123 45 67.",
  };
  const errorFor = (el) => {
    const v = el.validity;
    if (v.valid) return "";
    if (el.type === "checkbox" && v.valueMissing) return "Du behöver godkänna för att jag ska kunna svara dig.";
    if (v.valueMissing) return messages.valueMissing;
    if (v.typeMismatch) return messages.typeMismatch[el.type] || "Kontrollera fältet.";
    if (v.rangeUnderflow) return messages.rangeUnderflow;
    if (v.patternMismatch) return messages.patternMismatch;
    if (v.rangeOverflow || v.badInput) return "Kontrollera värdet.";
    return "Kontrollera fältet.";
  };
  const showError = (el) => {
    const wrap = el.closest(".field, .consent-field");
    const out = wrap && wrap.querySelector(".error");
    const msg = errorFor(el);
    if (out) out.textContent = msg;
    if (wrap) wrap.classList.toggle("is-invalid", !!msg);
    el.setAttribute("aria-invalid", msg ? "true" : "false");
    return !msg;
  };
  form.querySelectorAll("input, select, textarea").forEach((el) => {
    el.addEventListener("blur", () => { if (el.value || el.type === "checkbox") showError(el); });
    el.addEventListener("input", () => { if (el.getAttribute("aria-invalid") === "true") showError(el); });
  });

  const summary = (data) => {
    const lines = [
      ["Tillfälle", occasion.options[occasion.selectedIndex].text],
      ["Datum", data.get("datum")],
      ["Antal gäster/bitar", data.get("antal")],
      ["Hämtning eller leverans", data.get("leverans")],
      ["Leveransadress", data.get("adress")],
      ["Smaker", data.get("smaker")],
      ["Inspiration", data.get("inspiration")],
      ["Meddelande", data.get("meddelande")],
      ["Namn", data.get("namn")],
      ["Telefon", data.get("telefon")],
      ["E-post", data.get("epost")],
    ];
    return lines.filter(([, v]) => v).map(([k, v]) => k + ": " + v).join("\n");
  };

  const showStatus = (kind, html) => {
    status.className = "form-status" + (kind === "error" ? " form-status--error" : "");
    status.innerHTML = html;
    status.hidden = false;
    status.focus();
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    let firstBad = null;
    form.querySelectorAll("input, select, textarea").forEach((el) => {
      if (el.closest("[hidden]")) return;
      if (!showError(el) && !firstBad) firstBad = el;
    });
    if (firstBad) { firstBad.focus(); return; }

    const data = new FormData(form);
    if (data.get("_gotcha")) return; // honeypot
    const endpoint = form.dataset.endpoint;
    const subject = "Offertförfrågan: " + occasion.options[occasion.selectedIndex].text + " " + (data.get("datum") || "");

    if (!endpoint) {
      const body = "Hej Fiona,\n\nJag vill gärna ha en offert.\n\n" + summary(data) + "\n";
      window.location.href = "mailto:kontakt@fionasbakery.se?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      showStatus("ok",
        "<h2>Nästan klart</h2><p>Ditt e-postprogram öppnas med förfrågan ifylld. Tryck på skicka där, så återkommer jag inom ett par dagar.</p>" +
        "<p class=\"muted\">Öppnades inget? Mejla <a href=\"mailto:kontakt@fionasbakery.se\">kontakt@fionasbakery.se</a> eller ring 073-874 03 78.</p>");
      return;
    }

    submit.setAttribute("aria-busy", "true");
    submit.querySelector("span").textContent = "Skickar...";
    try {
      data.append("_subject", subject);
      const res = await fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } });
      if (!res.ok) throw new Error(String(res.status));
      form.reset();
      form.hidden = true;
      showStatus("ok", "<h2>Tack, förfrågan är skickad</h2><p>Jag återkommer med en offert inom ett par dagar. Har du bilder på hur tårtan ska se ut får du gärna skicka dem när jag svarat.</p>");
    } catch (err) {
      showStatus("error", "<h2>Förfrågan kunde inte skickas</h2><p>Något gick fel på vägen. Försök igen om en stund, eller mejla <a href=\"mailto:kontakt@fionasbakery.se\">kontakt@fionasbakery.se</a> direkt.</p>");
    } finally {
      submit.removeAttribute("aria-busy");
      submit.querySelector("span").textContent = "Skicka förfrågan";
    }
  });
})();
