import React, { useEffect } from 'react';

function Slideshow() {
  useEffect(() => {
    const slideshow = document.querySelector('.slideshow');
    const images = slideshow.querySelectorAll('img');
    console.log(images);
    let currentIndex = 0;

    images[currentIndex].classList.add('active');

    const interval = setInterval(() => {
      images[currentIndex].classList.remove('active');
      currentIndex = (currentIndex + 1) % images.length;
      images[currentIndex].classList.add('active');
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="slideshow">
      <img src="/assets/Kamara.jpg" alt="Kamara" />
      <img src="/assets/Tyrann Mathieu.jpg" alt="Tyrann Mathieu" />
      <img src="/assets/ohtani.jpg" alt="ohtani" />
      <img src="/assets/Lebron.jpg" alt="Lebron" />
    </div>
  );
}

export default Slideshow;