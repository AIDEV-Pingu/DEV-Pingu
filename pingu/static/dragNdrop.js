document.addEventListener('DOMContentLoaded', function () {
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

    imageContainer.addEventListener('click', () => {
        fileInput.click();
    });

    function allowDrop(event) {
        event.preventDefault();
        dropArea.style.border = '2px dashed #000';
    }

    function handleDrop(file) {
        if (file && file.type.startsWith('image/')) {
            fileInput.files = [file];
            const imageUrl = URL.createObjectURL(file);
            imageContainer.innerHTML = `<img src="${imageUrl}" style="max-width: 100%;" alt="Dropped Image">`;
        } else {
            alert('Please drop a valid image file.');
        }
    }
});