document
    .getElementById("uploadForm")
    .addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent the default form submission

        // get loading_indicator element from dom
        loading_indicator = document.getElementById("loading_indicator");

        // show loading indicator
        loading_indicator.style.display = "block";

        const formData = new FormData(this);
        const response = await fetch("/process-image", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        const messageElement = document.getElementById("message");

        if (response.status === 200) {
            //     messageElement.innerHTML = `<div class="alert alert-success" role="alert">
            //       File uploaded successfully: ${result.file}
            //   </div>`;
            // hide loading indicator
            loading_indicator.style.display = "none";
            initializeCarousel(result);
        } else {
            // hide loading indicator
            loading_indicator.style.display = "none";
            messageElement.innerHTML = `<div class="alert alert-danger" role="alert">
              Error: ${result.detail || "Unknown error"}
          </div>`;
        }
    });


