document.getElementById('imageUpload').addEventListener('change', async function (event) {
    const file = event.target.files[0];

    if (file) {
        console.log("Processing the image...");

        try {
            const base64Image = await compressAndConvertToBase64(file);
            const response = await fetch('/upload_custom_logo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: base64Image }),
            });

            if (response.ok) {
                console.log("Image uploaded successfully!");
            } else {
                console.error("Failed to upload image.");
            }
        } catch (error) {
            console.error("Error processing the image:", error);
        }
    }
});

async function compressAndConvertToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');

                const MAX_WIDTH = 800;
                const MAX_HEIGHT = 800;

                let width = img.width;
                let height = img.height;

                if (width > MAX_WIDTH || height > MAX_HEIGHT) {
                    if (width > height) {
                        height = (MAX_WIDTH / width) * height;
                        width = MAX_WIDTH;
                    } else {
                        width = (MAX_HEIGHT / height) * width;
                        height = MAX_HEIGHT;
                    }
                }

                canvas.width = width;
                canvas.height = height;

                ctx.drawImage(img, 0, 0, width, height);
                const base64Image = canvas.toDataURL('image/jpeg', 0.8);
                resolve(base64Image);
            };
            img.onerror = (error) => reject(error);
            img.src = e.target.result;
        };

        reader.onerror = (error) => reject(error);
        reader.readAsDataURL(file);
    });
}
