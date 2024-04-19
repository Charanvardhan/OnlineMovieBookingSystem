/**
 * Template Name: PhotoFolio
 * Updated: Jan 29 2024 with Bootstrap v5.3.2
 * Template URL: https://bootstrapmade.com/photofolio-bootstrap-photography-website-template/
 * Author: BootstrapMade.com
 * License: https://bootstrapmade.com/license/
 */
document.addEventListener("DOMContentLoaded", () => {
  ("use strict");

  /**
   * Preloader
   */
  const preloader = document.querySelector("#preloader");
  if (preloader) {
    window.addEventListener("load", () => {
      setTimeout(() => {
        preloader.classList.add("loaded");
      }, 1000);
      setTimeout(() => {
        preloader.remove();
      }, 2000);
    });
  }

  /**
   * Mobile nav toggle
   */
  const mobileNavShow = document.querySelector(".mobile-nav-show");
  const mobileNavHide = document.querySelector(".mobile-nav-hide");

  document.querySelectorAll(".mobile-nav-toggle").forEach((el) => {
    el.addEventListener("click", function (event) {
      event.preventDefault();
      mobileNavToogle();
    });
  });

  function mobileNavToogle() {
    document.querySelector("body").classList.toggle("mobile-nav-active");
    mobileNavShow.classList.toggle("d-none");
    mobileNavHide.classList.toggle("d-none");
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll("#navbar a").forEach((navbarlink) => {
    if (!navbarlink.hash) return;

    let section = document.querySelector(navbarlink.hash);
    if (!section) return;

    navbarlink.addEventListener("click", () => {
      if (document.querySelector(".mobile-nav-active")) {
        mobileNavToogle();
      }
    });
  });

  /**
   * Toggle mobile nav dropdowns
   */
  const navDropdowns = document.querySelectorAll(".navbar .dropdown > a");

  navDropdowns.forEach((el) => {
    el.addEventListener("click", function (event) {
      if (document.querySelector(".mobile-nav-active")) {
        event.preventDefault();
        this.classList.toggle("active");
        this.nextElementSibling.classList.toggle("dropdown-active");

        let dropDownIndicator = this.querySelector(".dropdown-indicator");
        dropDownIndicator.classList.toggle("bi-chevron-up");
        dropDownIndicator.classList.toggle("bi-chevron-down");
      }
    });
  });

  /**
   * Scroll top button
   */
  const scrollTop = document.querySelector(".scroll-top");
  if (scrollTop) {
    const togglescrollTop = function () {
      window.scrollY > 100
        ? scrollTop.classList.add("active")
        : scrollTop.classList.remove("active");
    };
    window.addEventListener("load", togglescrollTop);
    document.addEventListener("scroll", togglescrollTop);
    scrollTop.addEventListener(
      "click",
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      })
    );
  }

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: ".glightbox",
  });

  /**
   * Init swiper slider with 1 slide at once in desktop view
   */
  new Swiper(".slides-1", {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    slidesPerView: "auto",
    pagination: {
      el: ".swiper-pagination",
      type: "bullets",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });

  /**
   * Init swiper slider with 3 slides at once in desktop view
   */
  new Swiper(".slides-3", {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    slidesPerView: "auto",
    pagination: {
      el: ".swiper-pagination",
      type: "bullets",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
        spaceBetween: 40,
      },

      1200: {
        slidesPerView: 3,
      },
    },
  });

  /**
   * Animation on scroll function and init
   */
  function aos_init() {
    AOS.init({
      duration: 1000,
      easing: "ease-in-out",
      once: true,
      mirror: false,
    });
  }
  window.addEventListener("load", () => {
    aos_init();
  });

  /**
   * Seat selection
   */
  const seatsContainer = document.querySelector(".seatsContainer");
  const seats = document.querySelectorAll(".row .seat:not(.occupied)");
  const count = document.getElementById("count");
  const total = document.getElementById("total");
  const movieSelect = document.getElementById("movie");

  let ticketPrice = +movieSelect.value;

  //Update total and count
  function updateSelectedCount() {
    const selectedSeats = document.querySelectorAll(".row .seat.selected");
    const selectedSeatsCount = selectedSeats.length;
    count.innerText = selectedSeatsCount;
    total.innerText = selectedSeatsCount * ticketPrice;
  }

  //Movie Select Event
  movieSelect.addEventListener("change", (e) => {
    ticketPrice = +e.target.value;
    updateSelectedCount();
  });

  //Seat click event
  seatsContainer.addEventListener("click", (e) => {
    if (
      e.target.classList.contains("seat") &&
      !e.target.classList.contains("occupied")
    ) {
      e.target.classList.toggle("selected");
    }
    updateSelectedCount();
  });
  // Select the input element
  const movieSearchInput = document.getElementById("movieSearchInput");

  // Initialize a variable to store the input value
  let userInput = "";

  // Add an event listener to the input element
  movieSearchInput.addEventListener("input", function (event) {
    // Update the userInput variable with the current value of the input
    userInput = event.target.value;

    // Optionally, you can log the userInput variable to see the current input
    console.log(userInput);
  });
});

// Function to fetch data from a Django URL
function fetchData(movieId) {
  // Construct the URL to fetch from, including the movie ID
  var url = `users/show/${movieId}/`; // Update with your actual URL path

  console.log(url)
  
  // Use the Fetch API to get data from the server
  fetch(url)
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json(); // Assuming the server returns JSON data
  })
  .then(data => {
      // Handle the data you get back
      console.log(data); // Example: Log data to console
      updateUI(data);
  })
  .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
  });
}

function updateUI(data) {
  const show = data.show;
  const showtimes = data.showtimes;

  // Update modal title and synopsis
  document.querySelector(".modal-body h2").textContent = "Movie Title"; // Replace with actual title if available in response
  document.querySelector(".modal-body .movieSynopsis p").textContent = "Movie synopsis here..."; // Replace with actual synopsis

  // Update showtimes dropdown
  const showtimeSelect = document.getElementById("movie");
  showtimeSelect.innerHTML = "<option value='0'>Select here</option>"; // Reset dropdown
  showtimes.forEach(time => {
      let option = document.createElement("option");
      option.value = time;
      option.textContent = time; // Format as needed
      showtimeSelect.appendChild(option);
  });

  // Update showroom details if necessary
  document.querySelector("#exampleModal .modal-body .showroom-number").textContent = `Showroom Number: ${show.showroom.showroom_number}`;
  document.querySelector("#exampleModal .modal-body .seats").textContent = `Seats Available: ${show.showroom.seats}`;
  
  // Update formatted showtimes
  document.querySelector("#exampleModal .modal-body .formatted-times").textContent = show.showtime.formatted_times;
}