// script.js
async function processImage() {
    console.log('Button clicked!');
    const resultContainer = document.getElementById('result-container');

    try {
        // Generate a timestamp to ensure a fresh image is requested
        const timestamp = new Date().getTime();

        const response = await fetch(`/generate_board?timestamp=${timestamp}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const responseData = await response.json();

            resultContainer.innerHTML = "Board generated successfully.";

            // Remove existing image if present
            const existingImage = document.getElementById('generated-image');
            if (existingImage) {
                existingImage.remove();
            }

            // Create and display the new image
            const imgElement = document.createElement('img');
            imgElement.id = 'generated-image';
            imgElement.src = `${responseData.image_path}?timestamp=${timestamp}`;
            resultContainer.appendChild(imgElement);
        } else {
            resultContainer.innerHTML = "Failed to generate the board.";
        }
    } catch (error) {
        console.error('Error generating board:', error);
    }
}
