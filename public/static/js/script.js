document
    .getElementById("uploadForm")
    .addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent the default form submission
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
            initializeCarousel(result);
        } else {
            messageElement.innerHTML = `<div class="alert alert-danger" role="alert">
              Error: ${result.detail || "Unknown error"}
          </div>`;
        }
    });


