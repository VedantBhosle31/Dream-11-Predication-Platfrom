import * as React from "react";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import { useState } from "react";

const style = {
  position: "absolute",
  bottom: "10%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "#1E1E1E",
  border: "2px solid black",
  boxShadow: 24,
  p: 4,
  display: "flex",
  justifyContent: "space-between",
  fontFamily:"Montserrat",
//   color:"white"
borderRadius:"10px",
zIndex:100

};

interface ModalProps {
  open: boolean;
  handleDevClose: () => void;
}

const DevTools: React.FC<ModalProps> = ({ open, handleDevClose }) => {
  const [firstDropdown, setFirstDropdown] = useState("");
  const [secondDropdown, setSecondDropdown] = useState("");

  const handleFirstDropdownChange = (
    e: React.ChangeEvent<HTMLSelectElement>
  ) => {
    setFirstDropdown(e.target.value);
  };

  const handleSecondDropdownChange = (
    e: React.ChangeEvent<HTMLSelectElement>
  ) => {
    setSecondDropdown(e.target.value);
  };

  return (
    <Modal
      open={open}
      onClose={handleDevClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        <div style={{ width: "45%" }}>
          <label htmlFor="firstDropdown" style={{ color:"white"}}>Select Plan:</label>
          <select
            id="firstDropdown"
            value={firstDropdown}
            onChange={handleFirstDropdownChange}
            color="black"
          >
            <option value="Premium">Premium</option>
            <option value="Free">Free</option>
          </select>
        </div>

        <div style={{ width: "45%" }}>
          <label htmlFor="secondDropdown" style={{ color:"white"}}>Select Graph</label>
          <select
            id="secondDropdown"
            value={secondDropdown}
            onChange={handleSecondDropdownChange}
            color="black"
          >
            <option value="Knowledge">Knowledge</option>
            <option value="Alternate">Alternate</option>
          </select>
        </div>
      </Box>
    </Modal>
  );
};

export default DevTools;
