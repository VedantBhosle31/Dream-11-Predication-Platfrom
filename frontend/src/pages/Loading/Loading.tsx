// Loading.jsx
import { motion } from "framer-motion";
import "./Loading.css";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Loading = () => {
  const navigation = useNavigate();
  // Fade in with stagger
  const container = {
    hidden: { opacity: 0, y: 25 },
    show: {
      opacity: 1,
      y: 0,
      transition: {
        staggerChildren: 0.2,
        duration: 2,
      },
    },
  };

  useEffect(() => {
    // Navigate to team page after 3 seconds
    setTimeout(() => {
      navigation("/team");
    }, 3000);
  }, [navigation]);

  return (
    <motion.div
      // Fade in with stagger
      variants={container}
      animate="show"
      initial="hidden"
      className="video-container"
    >
      <video
        src="/loading.mp4"
        autoPlay
        loop
        muted
        playsInline
        controls={false}
      />
      <div className="content-container">
        <img className="dream11-logo" src="/logo.png" alt="" />
        <p>
          " Virat Kohli is an Indian international cricketer who plays Test and
          ODI cricket for the Indian national team. A former captain in all
          formats of the game in cricket in india and inter.. "
        </p>
      </div>
    </motion.div>
  );
};

export default Loading;
