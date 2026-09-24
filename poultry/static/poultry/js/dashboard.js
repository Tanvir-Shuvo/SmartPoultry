document.addEventListener("DOMContentLoaded", function () {

    const track = document.getElementById("farmCarouselTrack");
    const prevButton = document.getElementById("farmPrevButton");
    const nextButton = document.getElementById("farmNextButton");

    if (!track || !prevButton || !nextButton) {
        return;
    }

    const slides = track.querySelectorAll(".farm-carousel-slide");

    if (slides.length === 0) {
        prevButton.style.display = "none";
        nextButton.style.display = "none";

        return;
    }


    let currentIndex = 0;


    function getVisibleSlides() {

        if (window.innerWidth <= 700) {
            return 1;
        }

        if (window.innerWidth <= 1000) {
            return 2;
        }

        return 3;
    }


    function getMaxIndex() {

        const visibleSlides = getVisibleSlides();

        return Math.max(
            0,
            slides.length - visibleSlides
        );
    }


    function updateCarousel() {

        const visibleSlides = getVisibleSlides();

        const gap = 20;

        const slideWidth =
            (track.parentElement.clientWidth -
                gap * (visibleSlides - 1))
            / visibleSlides;

        const moveAmount =
            slideWidth + gap;

        track.style.transform =
            `translateX(-${currentIndex * moveAmount}px)`;


        const maxIndex = getMaxIndex();


        prevButton.disabled =
            currentIndex === 0;

        nextButton.disabled =
            currentIndex >= maxIndex;


        if (slides.length <= visibleSlides) {

            prevButton.style.display = "none";
            nextButton.style.display = "none";

        } else {

            prevButton.style.display = "flex";
            nextButton.style.display = "flex";

        }

    }


    nextButton.addEventListener("click", function () {

        const maxIndex = getMaxIndex();

        if (currentIndex < maxIndex) {

            currentIndex++;

            updateCarousel();

        }

    });


    prevButton.addEventListener("click", function () {

        if (currentIndex > 0) {

            currentIndex--;

            updateCarousel();

        }

    });


    window.addEventListener("resize", function () {

        const maxIndex = getMaxIndex();

        if (currentIndex > maxIndex) {
            currentIndex = maxIndex;
        }

        updateCarousel();

    });


    updateCarousel();

});