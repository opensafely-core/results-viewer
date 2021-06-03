import "./style.css";

// stupid simple show/hide links
for (const trigger of document.querySelectorAll("[data-show]")) {
  const to_show = document.getElementById(trigger.dataset.show);
  const to_hide = Array.from(document.querySelectorAll(trigger.dataset.hide));
  const to_unlight = Array.from(
    document.querySelectorAll(trigger.dataset.highlight)
  );
  const to_load = Array.from(to_show.querySelectorAll("[data-load]"));

  trigger.onclick = (e) => {
    to_load.forEach((l) => load(l));

    if (to_hide.length > 0) {
      // hide all others, then show current
      to_hide.forEach((h) => h.classList.remove("active"));
      to_show.classList.add("active");
    } else {
      // just show it, don't hide anything else
      to_show.classList.toggle("active");
    }
    if (to_unlight.length > 0) {
      to_unlight.forEach((u) => u.classList.remove("highlight"));
    }
    trigger.classList.add("highlight");
    e.stopPropagation();
  };
}

function load(elem) {
  if (elem.dataset.loaded) return;

  if (elem.src !== undefined) {
    // <img> or <iframe>
    elem.src = elem.dataset.load;
    return;
  }

  // text, log, or html
  fetch(elem.dataset.load, { mode: "no-cors" })
    .then((response) => response.text())
    .then((text) => {
      elem.innerHTML = text;
      elem.dataset.loaded = true;
    });
}

Array.from(document.querySelectorAll("iframe")).forEach((iframe) => {
  iframe.onload = function () {
    console.log(iframe.contentDocument.body.scrollHeight);
    console.log(iframe.contentDocument.body.scrollWidth);
    iframe.style.height = iframe.contentDocument.body.scrollHeight + "px";
    iframe.style.width = iframe.contentDocument.body.scrollWidth + "px";
  };
});
