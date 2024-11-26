import { BrowserRouter, Routes, Route } from "react-router";

import "./App.css";

import Home from "./pages/Home/Home";
import Loading from "./pages/Loading/Loading";
import TeamPage from "./pages/teamPage/teamPage";
import PlayerInfo from "./pages/player_display_card/displayCard";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/loading" element={<Loading />} />
        <Route path="/team" element={<TeamPage />} />
        <Route path="/player-info" element={<PlayerInfo />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
