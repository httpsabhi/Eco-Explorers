let login = document.querySelector(".login-form");

document.querySelector("#login-btn").onclick = () => {
  login.classList.toggle("active");
  navbar.classList.remove("active");
};

let navbar = document.querySelector(".header .navbar");

document.querySelector("#menu-btn").onclick = () => {
  login.classList.remove("active");
  navbar.classList.toggle("active");
};

window.onscroll = () => {
  login.classList.remove("active");
  navbar.classList.remove("active");
};

var swiper = new Swiper(".gallery-slider", {
  grabCursor: true,
  loop: true,
  centeredSlides: true,
  spaceBetween: 20,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    700: {
      slidesPerView: 2,
    },
  },
});

// Accuracy Bar
function progressBar(progressVal, totalPercentageVal = 100) {
  const strokeVal = (4.64 * 100) / totalPercentageVal;
  $(".progress-circle-prog").css(
    "stroke-dasharray",
    progressVal * strokeVal + " 999"
  );
  const el = $(".progress-text");
  const from = el.data("progress");
  el.data("progress", progressVal);
  const start = new Date().getTime();

  setTimeout(function () {
    const now = new Date().getTime() - start;
    const progress = now / 700;
    el.html((progressVal / totalPercentageVal) * 100 + "%");
    if (progress < 1) setTimeout(arguments.callee, 10);
  }, 10);
}

// Display Result
function predict() {
  const formData = new FormData($("#image-form")[0]);
  // console.log(formData);
  $("#result").html("");
  $("#predict-loader").show();
  $.ajax({
    url: "/result",
    type: "POST",
    data: formData,
    contentType: false,
    processData: false,
    success: function (response) {
      $("#predict-loader").hide();
      $("#result").html(response.result[0]);
      // console.log(response);
      progressBar(response.result[1].toFixed(2), 100);
    },
    error: function (xhr, status, error) {
      $("#predict-loader").hide();
      alert(
        "An error occurred while processing the request. Please try again later."
      );
    },
  });
}

// Display Uploaded Image
let InputFile = document.getElementById("image-upload");
let ImageUpload = document.getElementById("uploaded-image");

InputFile.addEventListener("change", function () {
  if (this.files && this.files[0]) {
    ImageUpload.src = URL.createObjectURL(this.files[0]);
  }
});

document.addEventListener("click", function (e) {
  const dropdown = document.querySelector(".dropdown-checkboxes-content");
  const button = document.querySelector(".dropdown-checkboxes button");

  if (button.contains(e.target)) {
    dropdown.style.display =
      dropdown.style.display === "flex" ? "none" : "flex";
  } else if (!dropdown.contains(e.target)) {
    dropdown.style.display = "none";
  }
});

// Conservation Status
function Conservation() {
  const formData = new FormData($("#conservation-form")[0]);
  // console.log(formData);
  $("#conservation-result").html("");
  $("#conservation-loader").show();
  $.ajax({
    url: "/conservation",
    type: "POST",
    data: formData,
    contentType: false,
    processData: false,
    success: function (response) {
      $("#conservation-loader").hide();
      $("#conservation-result").html(response.status);
      console.log(response);
    },
    error: function (xhr, status, error) {
      $("#conservation-loader").hide();
      alert(
        "An error occurred while processing the request. Please try again later."
      );
    },
  });
}