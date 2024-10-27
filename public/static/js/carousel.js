// static/js/carousel.js

// Function to initialize the Bootstrap carousel
function initializeCarousel(images) {
    const carouselContainer = document.getElementById("carouselContainer");

    // Clear any existing content
    carouselContainer.innerHTML = '';

    // Create carousel HTML structure
    let carouselHTML = `
        <div id="carouselExample" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">`;

    // Add each image as a carousel item
    images.forEach((image, index) => {
        carouselHTML += `
            <div class="carousel-item ${index === 0 ? 'active' : ''}">
                <img src="${image}" class="d-block w-100" alt="Page ${index + 1}">
                <div class="carousel-caption" style="background:black;opacity:0.7;">
                <p>This is a carousel caption</p>
                </div>
            </div>
        `;
    });

    // Add carousel controls (optional)
    carouselHTML += `
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
            </button>
        </div>
    `;

    // Insert carousel into the container
    carouselContainer.innerHTML = carouselHTML;

    // Initialize carousel with custom options
    const carouselElement = document.getElementById('carouselExample');
    const carouselInstance = new bootstrap.Carousel(carouselElement, {
        interval: 60000,   // Set interval between slides in milliseconds (e.g., 3000 for 3 seconds)
        wrap: false,       // Enables looping of slides
        pause: 'hover',    // Pauses carousel on hover
        keyboard: true
    });

    // Add an event listener to detect slide changes
    carouselElement.addEventListener('slide.bs.carousel', function (event) {
        console.log(`Slide changed to index: ${event.to}`);
        // Custom action on slide change
        // For example, update a counter or trigger audio narration for the new slide
    });
}
