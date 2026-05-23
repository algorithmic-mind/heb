
  document.addEventListener('DOMContentLoaded', function() {
  new Swiper('.logo-swiper', {
    slidesPerView: 3,
    spaceBetween: 20,
    loop: true,
    autoplay: {
      delay: 2500,
      disableOnInteraction: false,
    },
    breakpoints: {
      576: {
        slidesPerView: 3,
      },
      768: {
        slidesPerView: 4,
      },
      992: {
        slidesPerView: 5,
      },
      1200: {
        slidesPerView: 5,
      }
    }
  });
});

document.addEventListener('DOMContentLoaded', function() {
  new Swiper('.mySwiper', {
    slidesPerView: 1, // پیشفرض برای موبایل
    spaceBetween: 10,
    centeredSlides: false, // غیرفعال کردن حالت centered
    grabCursor: true,
    loop: false, // غیرفعال کردن loop اگر مشکل persist کند
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      768: {
        slidesPerView: 3,
        spaceBetween: 15
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 20
      }
    }
  });
});


