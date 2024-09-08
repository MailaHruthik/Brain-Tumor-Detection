// static/script.js

document.addEventListener("DOMContentLoaded", function() {
    const imageUpload = document.getElementById("image-upload");
    imageUpload.addEventListener("change", showSelectedImage);
  });
  
  function showSelectedImage(event) {
    const imageInput = event.target;
    const selectedImage = document.getElementById("selected-image");
  
    if (imageInput.files && imageInput.files[0]) {
      const reader = new FileReader();
      reader.onload = function (e) {
        selectedImage.src = e.target.result;
        selectedImage.style.display = "block"; // Display the image
      };
      reader.readAsDataURL(imageInput.files[0]);
    }
  }
  