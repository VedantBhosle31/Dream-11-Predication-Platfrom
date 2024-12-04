import { BrowserRouter, Routes, Route } from "react-router";

import "./App.css";
import Navbar from "./components/navbar/navbar";
import Home from "./pages/Home/Home";
import Loading from "./pages/Loading/Loading";
import TeamPage from "./pages/teamPage/teamPage";
import PlayerInfo from "./pages/player_display_card/displayCard";
import SlidingPanels from "./SlidingPanels";
import VideoPage from "./components/video_player/videopage";

const App = () => {
  return (
    <BrowserRouter>
      <div style={{ width: "100%" }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/loading" element={<Loading />} />
          <Route path="/team" element={<SlidingPanels />} />
          <Route path="/player-info" element={<PlayerInfo />} />
          <Route path="/videopage" element={<VideoPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
