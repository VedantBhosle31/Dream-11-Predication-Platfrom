import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import DisplayCardExpanded from "../player_display_card/displayCardExpanded2";

const Slideshow = () => {
  // Array of image and audio files
  const slides = [
    { image: "/slide1.jpg", audio: "/audio.mp3" },
    { image: "/slide2.jpg", audio: "/audio.mp3" },
    { image: "/slide3.jpg", audio: "/audio.mp3" },
    { image: "/slide4.jpg", audio: "/audio.mp3" },
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
    }, 15000);

    return () => clearInterval(timer); // Cleanup on unmount
  }, [slides.length]);

  return (
    <div className="flex flex-col items-center justify-center h-full p-4 w-full ">
      {/* Image with Framer Motion Animation */}
      <div className="relative w-full h-[85%]">
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

      {/* Navigation Buttons */}
      <div className="flex mt-2 gap-2">
        {slides.map((_, index) => (
          <button
            key={index}
            onClick={() => changeSlide(index)}
            className={`w-4 h-4 rounded-full ${currentIndex === index
              ? "bg-gray-800 text-white"
              : "bg-gray-300 text-black"
              }`}
          >
            
          </button>
        ))}
      </div>

      {/* Audio Player */}
      <AudioPlayer audio={slides[currentIndex].audio} />
    </div>
  );
};

// extract audio such tht it doesnt rerender
const AudioPlayer = ({ audio }: { audio: string }) => {
  return (
    <audio controls playsInline autoPlay className="mt-3 w-3/4 max-w-md h-8">
      <source src={audio} type="audio/mp3" />
      Your browser does not support the audio element.
    </audio>
  );
}



export default Slideshow;
