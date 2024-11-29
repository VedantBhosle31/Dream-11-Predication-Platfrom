import React from "react";

interface VideoPlayerProps {
  videoUrl: string;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ videoUrl }) => {
  return (
    <div style={{ textAlign: "center", width: "100%", height: "100%", justifyItems:"center", alignContent:"center"}}>
      <video
        src={videoUrl}
        controls
        style={{ width: "90%", height: "100%" }}
      >
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default VideoPlayer;
