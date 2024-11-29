import React, { useEffect, useRef, useState } from "react";
import { motion, useAnimation } from "framer-motion";
import "./Home.css";
import Heading from "../../components/Heading";
import ChooseTeam from "../../components/ChooseTeam";

import DownArrowSvg from "../../assets/down_arrow.svg";

const Home: React.FC = () => {
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
          transition: { delay: 0.5, duration: 0.5 }, // Added delay
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

  const scrollDown = () => {
    window.scrollTo({
      top: window.innerHeight * 3,
      behavior: "smooth",
    });
  };

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
        <Heading />
      </motion.div>

      <motion.div
        className="flex justify-center w-full fixed z-20 bottom-6 cursor-pointer"
        initial={{ opacity: 1, y: 0 }}
        animate={titleControls}
      >
        <motion.img
          whileTap={{ scale: 0.9 }}
          whileHover={{ scale: 1.2 }}
          src={DownArrowSvg}
          height={30}
          alt=""
          onClick={scrollDown}
          className="h-12 w-12"
        />
      </motion.div>

      {/* Empty Box Section */}
      <motion.div
        className="box"
        initial={{ opacity: 0, y: 50 }}
        animate={boxControls}
      >
        <ChooseTeam />
      </motion.div>

      {/* Spacer for Scrolling */}
      <div className="spacer" />
    </div>
  );
};

export default Home;
