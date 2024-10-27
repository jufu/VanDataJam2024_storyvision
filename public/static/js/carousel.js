// static/js/carousel.js

// Function to preload an audio file
const preloadAudio = (url) => {
    return new Promise((resolve, reject) => {
        const audio = new Audio();
        audio.preload = 'auto';

        audio.oncanplaythrough = () => {
            console.log('Audio preloaded:', url);
            resolve(url);
        };

        audio.onerror = (error) => {
            console.error('Audio preload error:', error);
            reject(error);
        };

        audio.src = url;
        audio.load();
    });
};

// Function to initialize the Bootstrap carousel
const initializeCarousel = async ({ image_files, texts = [], audio_files = [], unique_id }) => {
    console.log('Initializing carousel with:', {
        imageCount: image_files.length,
        audioCount: audio_files.length,
        firstAudioFile: audio_files[0]
    });

    const carouselContainer = document.getElementById("carouselContainer");
    const audioPlayer = document.getElementById("audioPlayer");

    if (!audioPlayer) {
        console.error('Audio player element not found!');
        return;
    }

    // Preload the first audio file before continuing
    if (audio_files.length > 0 && audio_files[0]) {
        console.log('Preloading first audio file...');
        try {
            await preloadAudio(audio_files[0]);
        } catch (error) {
            console.error('Failed to preload first audio:', error);
        }
    }

    // Clear any existing content
    carouselContainer.innerHTML = '';

    // Create carousel HTML structure
    let carouselHTML = `
        <div id="carouselExample" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">`;

    image_files.forEach((image, index) => {
        carouselHTML += `
            <div class="carousel-item ${index === 0 ? 'active' : ''}">
                <img src="${image}" class="d-block w-100" alt="Page ${index + 1}">
                <div class="carousel-caption" style="background:black;opacity:0.7;">
                <p>${texts[index] || ""}</p>
                </div>
            </div>
        `;
    });

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

    carouselContainer.innerHTML = carouselHTML;

    // Initialize carousel
    const carouselElement = document.getElementById('carouselExample');
    const carouselInstance = new bootstrap.Carousel(carouselElement, {
        interval: 60000,  // No auto-slide
        wrap: false,
        pause: 'hover',
        keyboard: true
    });

    // Function to play audio
    const playAudio = (audioSrc) => {
        console.log('Playing audio:', audioSrc);
        audioPlayer.src = audioSrc;
        return audioPlayer.play().catch(error => {
            console.error('Audio playback failed:', error);
        });
    };

    // Play the first audio file immediately since it's preloaded
    if (audio_files.length > 0 && audio_files[0]) {
        console.log('Starting first audio playback');
        playAudio(audio_files[0]);
    }

    // Handle slide changes and play the corresponding audio
    carouselElement.addEventListener('slide.bs.carousel', function (event) {
        console.log(`Slide changing to index: ${event.to}`);

        // Check if there is a corresponding audio file for the slide index
        if (audio_files[event.to]) {
            playAudio(audio_files[event.to]);
        } else {
            console.warn(`No audio available for slide ${event.to}`);
        }
    });

    // Add audio event listeners for debugging
    audioPlayer.addEventListener('playing', () => {
        console.log('Audio started playing');
    });

    audioPlayer.addEventListener('waiting', () => {
        console.log('Audio is waiting for data');
    });

    audioPlayer.addEventListener('canplaythrough', () => {
        console.log('Audio can play through without buffering');
    });

    audioPlayer.addEventListener('error', (e) => {
        console.error('Audio error:', e.target.error);
    });
};
