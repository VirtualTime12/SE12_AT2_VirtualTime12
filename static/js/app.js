if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("/serviceworker.js")
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

document.addEventListener("DOMContentLoaded", () => {
  const dropdowns = document.querySelectorAll(".dropdown");
  dropdowns.forEach((dropdown) => {
    const button = dropdown.querySelector(".dropbtn");
    if (button) {
      button.addEventListener("click", myFunction);
    }
  });
});

function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function (event) {
  if (!event.target.matches(".dropbtn")) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains("show")) {
        openDropdown.classList.remove("show");
      }
    }
  }
};
