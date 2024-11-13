// Get the slideshow element
const slideshow = document.querySelector('.slideshow');

// Get the images in the slideshow
const images = slideshow.querySelectorAll('img');

// Set the first image as active
images[0].classList.add('active');

// Set the interval for the slideshow
setInterval(() => {
  // Get the current active image
  const currentImage = slideshow.querySelector('.active');

  // Remove the active class from the current image
  currentImage.classList.remove('active');

  // Get the next image
  const nextImage = currentImage.nextElementSibling || images[0];

  // Add the active class to the next image
  nextImage.classList.add('active');
}, 5000); // Set the interval to 5 seconds