const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const imageContainer = document.getElementById('image-container');

dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.style.border = '2px dashed #000';
});

dropArea.addEventListener('dragleave', () => {
    dropArea.style.border = '2px dashed #ccc';
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.style.border = '2px dashed #ccc';
    handleDrop(e.dataTransfer.files[0]);
});

fileInput.addEventListener('change', (e) => {
    handleDrop(e.target.files[0]);
});

function handleDrop(file) {
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (event) => {
            const imageUrl = event.target.result;
            displayImage(imageUrl);
        };
        reader.readAsDataURL(file);
    } else {
        alert('Please drop a valid image file.');
    }
}

function displayImage(url) {
    const img = new Image();
    img.src = url;
    img.style.maxWidth = '100%';
    imageContainer.innerHTML = '';
    imageContainer.appendChild(img);
}