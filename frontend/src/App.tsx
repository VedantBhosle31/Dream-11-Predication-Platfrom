import React from "react";
import { BrowserRouter, Routes, Route } from "react-router";
import Home from "./pages/Home";
import Loading from "./pages/Loading";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/loading" element={<Loading />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
