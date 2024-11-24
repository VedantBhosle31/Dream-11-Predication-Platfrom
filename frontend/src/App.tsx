import React, { useEffect, useRef, useState } from "react";
import { motion, useAnimation } from "framer-motion";
import "./App.css";

const App: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const titleControls = useAnimation();
  const boxControls = useAnimation();
  const [lastScrollY, setLastScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;

      // Title Animation
      if (currentScrollY < 100) {
        titleControls.start({
          opacity: 1,
          y: 0,
          transition: { duration: 0.5 },
        });
        boxControls.start({
          opacity: 0,
          y: 50,
          transition: { duration: 0.5 },
        });
      } else if (currentScrollY < 200) {
        titleControls.start({
          opacity: 0,
          y: -50,
          transition: { duration: 0.5 },
        });

        // Delay box fade-in
        boxControls.start({
          opacity: 1,
          y: 0,
          transition: { delay: 0.3, duration: 0.5 }, // Added delay
        });
      }

      // Video Scrubbing Logic
      const video = videoRef.current;
      if (video) {
        const totalHeight = document.body.scrollHeight - window.innerHeight;
        const scrollFraction = currentScrollY / totalHeight;
        video.currentTime = scrollFraction * (video.duration || 1);
      }

      setLastScrollY(currentScrollY);
    };

    // Attach Scroll Event Listener
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, [titleControls, boxControls, lastScrollY]);

  return (
    <div className="App" id="container">
      {/* Background Video */}
      <video
        ref={videoRef}
        className="background-video"
        loop
        muted
        src="bg_video.mp4"
      ></video>

      {/* Title Section */}
      <motion.div
        className="title"
        initial={{ opacity: 1, y: 0 }}
        animate={titleControls}
      >
        <h1>Big Title</h1>
      </motion.div>

      {/* Empty Box Section */}
      <motion.div
        className="box"
        initial={{ opacity: 0, y: 50 }}
        animate={boxControls}
      >
        <div>Content Fades In</div>
      </motion.div>

      {/* Spacer for Scrolling */}
      <div className="spacer" />
    </div>
  );
};

export default App;
