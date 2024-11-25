import React from "react";
import { motion, stagger } from "framer-motion";
import { useNavigate } from "react-router-dom";

type InputContainerProps = {
  label: string;
  children: React.ReactNode;
  id: string;
};

type FloatingImageProps = {
  src: string;
  alt: string;
  width?: number;
  first?: boolean;
};

const ChooseTeam = () => {
  return (
    <div>
      <motion.div animate={{}} className="top-container">
        <FloatingImage first src="/mi.png" alt="team_logo" />
        <div className="inputs-container">
          <InputContainer label="Choose Team 1" id="team1">
            <input type="search" />
          </InputContainer>
          <InputContainer label="Choose Team 2" id="team2">
            <input type="search" />
          </InputContainer>
          <InputContainer label="Choose Match Date" id="matchDate">
            <input type="date" style={{ width: 476 }} />
          </InputContainer>
        </div>
        <FloatingImage src="/rcb.png" alt="team_logo" />
      </motion.div>
      {/* AI button */}
      <div>
        <AnimatedButton />
      </div>
    </div>
  );
};

const FloatingImage: React.FC<FloatingImageProps> = ({
  src,
  alt,
  width = 250,
  first = false,
}) => {
  const floatingWithRotation = {
    y: [-10, 0, -10],
    rotate: [-1, 0, -1],
    transition: {
      duration: 5,
      ease: "easeInOut",
      repeat: Infinity,
      delay: first ? 0 : 2.5,
    },
  };

  return (
    <motion.img
      src={src}
      alt={alt}
      width={width}
      animate={floatingWithRotation}
      className="select-team-img"
      style={{
        width: width,
        height: "auto",
      }}
    />
  );
};

const AnimatedButton = () => {
  const navigate = useNavigate();

  return (
    <motion.button
      className="animated-button"
      initial={{
        background: "rgba(0, 0, 0, 0.25)",
        border: "1px solid rgba(255, 255, 255, 0.5)",
        color: "rgba(255, 255, 255, 0.5)",
      }}
      whileHover={{
        boxShadow: "-5px 5px 40px #ff5d6b",
        background: "#ff4141",
        color: "rgba(255, 255, 255)",
      }}
      whileTap={{
        scale: 0.99,
      }}
      onClick={() => {
        // delay the navigation by 1s
        setTimeout(() => {
          navigate("/loading");
        }, 400);
      }}
    >
      <motion.div
        className="button-gradient"
        initial={{
          opacity: 0,
        }}
        whileHover={{
          opacity: 1,
        }}
        transition={{
          duration: 0.8,
          ease: "easeOut",
        }}
      />
      Generate your Dream Team
    </motion.button>
  );
};

const InputContainer: React.FC<InputContainerProps> = ({
  children,
  label,
  id,
}) => {
  return (
    <div className="input-container">
      <label htmlFor={id}>{label}</label>
      {children}
    </div>
  );
};

export default ChooseTeam;
