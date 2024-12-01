import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

const Slideshow = () => {
  // Array of image and audio files
  const slides = [
    { image: "/slide1.jpg", audio: "/audio_0.mp3" },
    { image: "/slide2.jpg", audio: "/audio_1.mp3" },
    { image: "/slide3.jpg", audio: "/audio_2.mp3" },
    { image: "/slide4.jpg", audio: "/audio_3.mp3" },
  ];

  const [currentIndex, setCurrentIndex] = useState(0);

  // Function to switch slides
  const changeSlide = (index: number) => {
    setCurrentIndex(index);
  };

  // Auto-switch slide every 30 seconds
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % slides.length);
    }, 30000);

    return () => clearInterval(timer); // Cleanup on unmount
  }, [slides.length]);

  return (
    <div className="flex flex-col items-center justify-center h-full p-4 bg-transparent">
      {/* Image with Framer Motion Animation */}
      <div className="relative w-full h-96">
        <AnimatePresence mode="wait">
          <motion.img
            key={slides[currentIndex].image}
            src={slides[currentIndex].image}
            alt={`Slide ${currentIndex + 1}`}
            className="w-full h-full object-cover rounded-lg shadow-lg"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.5 }}
          />
        </AnimatePresence>
      </div>

      {/* Audio Player */}
      <audio
        key={currentIndex}
        controls
        autoPlay
        className="mt-5 w-3/4 max-w-md"
      >
        <source src={slides[currentIndex].audio} type="audio/mp3" />
        Your browser does not support the audio element.
      </audio>

      {/* Navigation Buttons */}
      <div className="flex gap-2 mt-5">
        {slides.map((_, index) => (
          <button
            key={index}
            onClick={() => changeSlide(index)}
            className={`w-8 h-8 rounded-full ${
              currentIndex === index
                ? "bg-gray-800 text-white"
                : "bg-gray-300 text-black"
            }`}
          >
            {index + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Slideshow;
