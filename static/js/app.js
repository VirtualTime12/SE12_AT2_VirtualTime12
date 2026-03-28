if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("static/js/serviceWorker.js")
      .then((res) => console.log("service worker registered"))
      .catch((err) => console.log("service worker not registered", err));
  });
}

function debounce(fn, delay = 300) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("mySearch");
  if (searchInput) {
    searchInput.addEventListener("input", debounce(filterVtubers, 300));
  }
});

function filterVtubers(event) {
  const query = event.target.value.toUpperCase();
  const cards = document.querySelectorAll(".card");

  cards.forEach((card) => {
    const nameEl = card.querySelector(".card-name");
    const nameText = nameEl ? nameEl.textContent.toUpperCase() : "";
    card.style.display = nameText.includes(query) ? "" : "none";
  });
}

//   const input = document.getElementById("mySearch");
//   const filter = input.value.toUpperCase();
//   const ul = document.getElementById("myMenu");
//   const li = ul.getElementsByTagName("li");

//   for (let i = 0; i < li.length; i++) {
//     const a = li[i].getElementsByTagName("a")[0];
//     li[i].style.display =
//       a.innerHTML.toUpperCase().indexOf(filter) > -1 ? "" : "none";
//   }
// }
