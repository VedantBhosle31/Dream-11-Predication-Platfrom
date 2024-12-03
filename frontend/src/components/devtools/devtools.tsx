// import React, { useState } from 'react';

// const DevTools = () => {
//   const [firstDropdown, setFirstDropdown] = useState('');
//   const [secondDropdown, setSecondDropdown] = useState('');

//   const handleFirstDropdownChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
//     setFirstDropdown(e.target.value);
//   };

//   const handleSecondDropdownChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
//     setSecondDropdown(e.target.value);
//   };

//   return (
//     <div style={styles.popupBackground}>
//       <div style={styles.popup}>
//         <h2>Select Options</h2>
//         <div style={styles.formGroup}>
//           <div style={styles.dropdown}>
//             <label htmlFor="firstDropdown">Select Plan:</label>
//             <select
//               id="firstDropdown"
//               value={firstDropdown}
//               onChange={handleFirstDropdownChange}
//             >
//               <option value="Premium">Premium</option>
//               <option value="Free">Free</option>
//             </select>
//           </div>

//           <div style={styles.dropdown}>
//             <label htmlFor="secondDropdown">Select Type:</label>
//             <select
//               id="secondDropdown"
//               value={secondDropdown}
//               onChange={handleSecondDropdownChange}
//             >
//               <option value="knowledge">Knowledge</option>
//               <option value="alternate">Alternate</option>
//             </select>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// const styles: { [key: string]: React.CSSProperties } = {
//   popupBackground: {
//     // position: 'fixed',
//     // top: 0,
//     // left: 0,
//     // right: 0,
//     // bottom: 0,
//     backgroundColor: 'rgba(0, 0, 0, 0.5)',
//     display: 'flex',
//     justifyContent: 'center',
//     alignItems: 'center',
//   },
//   popup: {
//     backgroundColor: 'white',
//     padding: '20px',
//     borderRadius: '8px',
//     width: '300px',
//     textAlign: 'center',
//   },
//   formGroup: {
//     display: 'flex',
//     justifyContent: 'space-between',
//   },
//   dropdown: {
//     width: '45%',
//   },
// };

// export default DevTools;

import * as React from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import { useState } from "react";
import { color } from "framer-motion";
import zIndex from "@mui/material/styles/zIndex";

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
  //   handleDevOpen: () => void;
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
