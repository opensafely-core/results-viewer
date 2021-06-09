import "alpinejs";
import "./style.css";
import prettyBytes from "pretty-bytes";

/**
 * Use Intl to format date and time
 */
[...document.querySelectorAll("[data-format='date-time']")].map((item) => {
  const initialDate = item.textContent;

  if (Date.parse(initialDate)) {
    const formattedDate = Intl.DateTimeFormat("en-GB", {
      dateStyle: "long",
      timeStyle: "short",
    }).format(new Date(new Date(initialDate)));
    item.textContent = formattedDate;
  }
});

/**
 * Use Pretty Bytes to format file sizes
 */
[...document.querySelectorAll("[data-format='file-size']")].map(
  (item) => (item.textContent = prettyBytes(parseInt(item.textContent)))
);
