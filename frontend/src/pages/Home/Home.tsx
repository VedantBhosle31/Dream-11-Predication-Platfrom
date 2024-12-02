import React, { useEffect, useRef, useState } from "react";
import { motion, useAnimation } from "framer-motion";
import "./Home.css";
import Heading from "../../components/Heading";
import ChooseTeam from "../../components/ChooseTeam";

import DownArrowSvg from "../../assets/down_arrow.svg";
import DevTools from "../../components/devtools/devtools";
import { Button } from "@mui/material";

const Home: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const titleControls = useAnimation();
  const boxControls = useAnimation();
  const [lastScrollY, setLastScrollY] = useState(0);

  var [devexpanded, setDevExpanded] = useState(false);
  const handleDevOpen = () => setDevExpanded(true);

  const handleDevClose = () => setDevExpanded(false);

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
        src="bg_video_2.mp4"
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
        className="down_arrow_svg"
        initial={{ opacity: 1, y: 0 }}
        animate={titleControls}
      >
        <motion.img
          whileTap={{ scale: 0.9 }}
          whileHover={{ scale: 1.2 }}
          src={DownArrowSvg}
          height={50}
          alt=""
          onClick={scrollDown}
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
