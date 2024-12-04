import React, { useEffect, useState } from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

interface CircularProgressProps {
  percentage: number;
}

const CircularProgress: React.FC<CircularProgressProps> = ({ percentage }) => {
  const [animatedPercentage, setAnimatedPercentage] = useState(0);

  useEffect(() => {
    const animationTimeout = setTimeout(() => {
      setAnimatedPercentage(percentage);
    }, 100); // Slight delay for smooth animation start
    return () => clearTimeout(animationTimeout); // Cleanup timeout on component unmount
  }, [percentage]);

  return (
    <div style={{ width: '100px', height: '100px' }}>
      <CircularProgressbar
        value={animatedPercentage}
        text={`${animatedPercentage}%`}
        styles={buildStyles({
          textColor: 'white',
          pathColor: 'red',
          trailColor: 'rgba(255, 255, 255, 0.1)',
          textSize: '16px',
          pathTransitionDuration: 1, // Duration of animation
        })}
      />
    </div>
  );
};

export default CircularProgress;
