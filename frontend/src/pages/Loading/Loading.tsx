import { motion } from "framer-motion";
import "./Loading.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import usePlayerStore from "../../store/playerStore";

const Loading = () => {
  const navigation = useNavigate();
  const { fetchBest11, playerNames } = usePlayerStore();
  const [playersFetched, setPlayersFetched] = useState(false);
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

  console.log(playerNames);

  useEffect(() => {
    async function fetchData() {
      await fetchBest11()
        .then((data) => data)
        .then(() => setPlayersFetched(true));
    }

    fetchData();
  }, [navigation, fetchBest11]);

  // Navigate to the next page if the best 11 players are fetched
  useEffect(() => {
    if (playersFetched) {
      navigation("/team");
    }
  }, [playersFetched]);

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
      <div className="flex w-full h-full z-20 absolute top-0 flex-col text-white justify-center items-center gap-y-4">
        <img className="dream11-logo" src="/logo.png" alt="" />
        <p className="text-xl max-w-[50%] text-center">
          " Virat Kohli is an Indian international cricketer who plays Test and
          ODI cricket for the Indian national team. A former captain in all
          formats of the game in cricket in india and inter.. "
        </p>
      </div>
    </motion.div>
  );
};

export default Loading;
