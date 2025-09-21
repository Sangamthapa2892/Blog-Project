document.addEventListener("DOMContentLoaded", function () {
  /* -------------------- 🔹 Navbar active link toggle -------------------- */
  const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
  navLinks.forEach((link) => {
    link.addEventListener("click", function () {
      navLinks.forEach((l) => l.classList.remove("active"));
      this.classList.add("active");
    });
  });

  /* -------------------- 🔹 Submit button disable + loading text -------------------- */
  const form = document.querySelector(".login-card");
  const submitBtn = form?.querySelector('button[type="submit"]');
  form?.addEventListener("submit", function () {
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = "Registering...";
    }
  });

  /* -------------------- 🔹 File input + preview logic -------------------- */
  const fileInput = document.getElementById("id_profile_image");
  const fileNameSpan = document.getElementById("file-name");
  const clearBtn = document.getElementById("clear-btn");
  const previewContainer = document.getElementById("preview-container");
  const previewImage = document.getElementById("preview-image");

  if (fileInput) {
    fileInput.style.display = "none"; // hide real input

    fileInput.addEventListener("change", function () {
      if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        fileNameSpan.textContent = file.name;
        clearBtn.style.display = "inline";

        // Show preview
        const reader = new FileReader();
        reader.onload = function (e) {
          previewImage.src = e.target.result;
          previewContainer.style.display = "block";
        };
        reader.readAsDataURL(file);
      } else {
        resetFileInput();
      }
    });

    window.clearFile = function (event) {
      event.stopPropagation();
      resetFileInput();
    };

    function resetFileInput() {
      fileInput.value = "";
      fileNameSpan.textContent = "Choose file...";
      clearBtn.style.display = "none";
      previewContainer.style.display = "none";
      previewImage.src = "#";
    }
  }

  /* -------------------- 🔹 Page loader fade-out -------------------- */
  const pageLoader = document.getElementById("pageLoader");
  if (pageLoader) {
    setTimeout(() => {
      pageLoader.classList.add("fade-out");
      setTimeout(() => {
        pageLoader.style.display = "none";
      }, 500);
    }, 800);
  }

  /* -------------------- 🔹 Scroll progress bar -------------------- */
  const scrollProgress = document.getElementById("scrollProgress");
  if (scrollProgress) {
    window.addEventListener("scroll", () => {
      const scrollPercent =
        (window.scrollY /
          (document.documentElement.scrollHeight - window.innerHeight)) *
        100;
      scrollProgress.style.width = scrollPercent + "%";
    });
  }

  /* -------------------- 🔹 Scroll to top button -------------------- */
  const scrollToTopBtn = document.getElementById("scrollToTop");
  if (scrollToTopBtn) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 300) {
        scrollToTopBtn.classList.add("visible");
      } else {
        scrollToTopBtn.classList.remove("visible");
      }
    });

    scrollToTopBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* -------------------- 🔹 Navbar scroll effect -------------------- */
  const navbar = document.getElementById("mainNavbar");
  if (navbar) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 50) {
        navbar.classList.add("scrolled");
      } else {
        navbar.classList.remove("scrolled");
      }
    });
  }

  /* -------------------- 🔹 Auto-dismiss alerts -------------------- */
  setTimeout(function () {
    const alertElement = document.getElementById("autoDismissAlert");
    if (alertElement) {
      const alertInstance = bootstrap.Alert.getOrCreateInstance(alertElement);
      alertInstance.close();
    }
  }, 3000);

  /* -------------------- 🔹 Staggered animation for cards -------------------- */
  const cards = document.querySelectorAll(".card");
  if (cards.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.style.animation = "fadeInUp 0.6s ease-out forwards";
          }, index * 100);
        }
      });
    });

    cards.forEach((card) => {
      card.style.opacity = "0";
      observer.observe(card);
    });
  }
});
const modal = new bootstrap.Modal(
  document.getElementById("deleteCommentModal{{ comment.id }}"),
  {
    backdrop: false,
  }
);
modal.show();
