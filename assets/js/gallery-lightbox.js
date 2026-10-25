(() => {
  const dialog = document.getElementById("gallery-lightbox");

  if (!dialog || typeof dialog.showModal !== "function") {
    return;
  }

  const image = dialog.querySelector("[data-gallery-image]");
  const caption = dialog.querySelector("[data-gallery-caption]");
  const counter = dialog.querySelector("[data-gallery-counter]");
  const previousButton = dialog.querySelector("[data-gallery-previous]");
  const nextButton = dialog.querySelector("[data-gallery-next]");
  let photos = [];
  let activeIndex = 0;

  const showPhoto = (index) => {
    activeIndex = (index + photos.length) % photos.length;
    const photo = photos[activeIndex];

    image.src = photo.href;
    image.alt = photo.dataset.alt || "";
    caption.textContent = photo.dataset.caption || "";
    counter.textContent = `${activeIndex + 1} / ${photos.length}`;
    previousButton.hidden = photos.length < 2;
    nextButton.hidden = photos.length < 2;
  };

  document.querySelectorAll("[data-gallery-open]").forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      photos = Array.from(link.closest(".event-gallery__item").querySelectorAll("[data-gallery-open]"));
      showPhoto(photos.indexOf(link));
      dialog.showModal();
    });
  });

  previousButton.addEventListener("click", () => showPhoto(activeIndex - 1));
  nextButton.addEventListener("click", () => showPhoto(activeIndex + 1));
  dialog.querySelector("[data-gallery-close]").addEventListener("click", () => dialog.close());

  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      dialog.close();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (!dialog.open) {
      return;
    }

    if (event.key === "ArrowLeft") {
      showPhoto(activeIndex - 1);
    } else if (event.key === "ArrowRight") {
      showPhoto(activeIndex + 1);
    } else if (event.key === "Escape") {
      event.preventDefault();
      dialog.close();
    }
  });
})();