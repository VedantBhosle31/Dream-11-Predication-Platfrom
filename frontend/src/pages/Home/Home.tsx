import React, { useEffect, useRef, useState } from "react";
import { motion, useAnimation } from "framer-motion";
import "./Home.css";
import Heading from "../../components/Heading";
import ChooseTeam from "../../components/choose-team/ChooseTeam";

import DownArrowSvg from "../../assets/down_arrow.svg";
import DevTools from "../../components/devtools/devtools";
import { Button } from "@mui/material";

const Home: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const titleControls = useAnimation();
  const boxControls = useAnimation();
  const [scrollY, setScrollY] = useState(0);
  const [devexpanded, setDevExpanded] = useState(false);

  const handleDevOpen = () => setDevExpanded(true);
  const handleDevClose = () => setDevExpanded(false);

  // Track scroll position
  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  // Handle animations
  useEffect(() => {
    if (scrollY < 100) {
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
    } else if (scrollY < 200) {
      titleControls.start({
        opacity: 0,
        y: -50,
        transition: { duration: 0.5 },
      });
      boxControls.start({
        opacity: 1,
        y: 0,
        transition: { delay: 0.5, duration: 0.5 },
      });
    }

    // Video scrubbing
    const video = videoRef.current;
    if (video) {
      const totalHeight = document.body.scrollHeight - window.innerHeight;
      const scrollFraction = scrollY / totalHeight;
      video.currentTime = scrollFraction * (video.duration || 1);
    }
  }, [scrollY, titleControls, boxControls]);

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
        className="flex justify-center w-full fixed z-20 bottom-20 cursor-pointer"
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

      {/* dev tools */}
      <motion.div className="devtools">
        <Button onClick={handleDevOpen}>Dev Tools</Button>
        <DevTools open={devexpanded} handleDevClose={handleDevClose} />
      </motion.div>
    </div>
  );
};

export default Home;
