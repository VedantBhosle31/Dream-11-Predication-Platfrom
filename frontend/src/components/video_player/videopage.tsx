import React, { useState } from "react";
import VideoPlayer from "./videoplayer";

const VideoPage: React.FC = () => {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  // Replace this with the actual URL of your Django backend
  const backendUrl = "http://127.0.0.1:8000/video/stream/stream_video.mp4";

  const loadVideo = () => {
    setVideoUrl(backendUrl);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Video Streaming App</h1>
      <button
        onClick={loadVideo}
        style={{
          padding: "10px 20px",
          margin: "20px",
          cursor: "pointer",
          backgroundColor: "#007BFF",
          color: "white",
          border: "none",
          borderRadius: "5px",
        }}
      >
        Load Video
      </button>
      {videoUrl && <VideoPlayer videoUrl={videoUrl} />}
    </div>
  );
};

export default VideoPage;
