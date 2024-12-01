import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { CloudUpload } from "lucide-react";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import * as XLSX from "xlsx";
import Papa from "papaparse";
import CustomSelect from "./MultiSelect";

const serverTeamLogos = {
  India: "/mi.png",
  SA: "/rcb.png",
};

const ChooseTeam = () => {
  const [file, setFile] = useState<File | null>(null);
  const [fileData, setFileData] = useState<any[]>([]);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [teamLogos, setTeamLogos] = useState<any>(null);
  const [manualSelection, setManualSelection] = useState(true);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateCSV = (data: any[]) => {
    // Check if headers match the required format
    const requiredHeaders = ["Player Name", "Squad", "Match Date", "Format"];
    const headers = Object.keys(data[0] || {});

    const headersMatch = requiredHeaders.every((header) =>
      headers.includes(header)
    );

    // Additional validation checks
    const isValid =
      headersMatch &&
      data.every(
        (row) =>
          row["Player Name"] &&
          row["Squad"] &&
          row["Match Date"] &&
          row["Format"]
      );

    return isValid;
  };

  // Handle file upload
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = event.target.files?.[0];
    if (!uploadedFile) return;
    setTeamLogos(null);
    setFile(uploadedFile);
    setUploadError(null);

    // Determine file type and parse accordingly
    const fileExtension = uploadedFile.name.split(".").pop()?.toLowerCase();

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result;

      try {
        let parsedData: any[];

        if (fileExtension === "csv") {
          // Parse CSV
          Papa.parse(content as string, {
            header: true,
            complete: (results: any) => {
              parsedData = results.data;
              processUploadedData(parsedData);
            },
          });
        } else if (["xlsx", "xls"].includes(fileExtension || "")) {
          // Parse Excel
          const workbook = XLSX.read(content, { type: "binary" });
          const sheetName = workbook.SheetNames[0];
          parsedData = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
          processUploadedData(parsedData);
        } else {
          throw new Error("Unsupported file type");
        }
      } catch (error) {
        setUploadError("Error parsing file. Please check the file format.");
      }
    };

    if (fileExtension === "csv") {
      reader.readAsText(uploadedFile);
    } else if (["xlsx", "xls"].includes(fileExtension || "")) {
      reader.readAsBinaryString(uploadedFile);
    }
  };

  // Process and validate uploaded data
  const processUploadedData = (data: any[]) => {
    if (validateCSV(data)) {
      setFileData(data);

      // // Simulate API call
      setTimeout(() => {
        setTeamLogos(serverTeamLogos);
      }, 1000);
    } else {
      setUploadError(
        "Invalid file format. Please upload a file with the correct structure."
      );
    }
  };

  if (manualSelection) {
    return <ChooseTeamManually />;
  } else {
    return (
      <div className="flex-center">
        {teamLogos && (
          <FloatingImage src={teamLogos.India} alt="team_logo" first />
        )}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="card"
        >
          {/* File Upload Section */}
          <div
            className="upload-box"
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              accept=".csv,.xlsx,.xls"
            />
            {!file && !fileData.length && (
              <>
                <CloudUpload className="upload-box-icon" size={48} />
                <p className="upload-box-text">
                  Drag and drop your Excel or CSV file here, or click to select
                </p>
                <p className="upload-box-subtext">
                  Supported formats: .csv, .xlsx, .xls
                </p>
              </>
            )}

            {file && (
              <div className="file-preview">
                <p className="file-name">{file.name}</p>

                {uploadError && <p className="error-box">{uploadError}</p>}

                {!uploadError && !teamLogos && (
                  <p className="file-preview-loading">Loading team logos...</p>
                )}
              </div>
            )}
          </div>

          {/* AI button */}

          <div className="btn-cont">
            <AnimatedButton
              disabled={(!file || !fileData || uploadError) as boolean}
            />
          </div>
        </motion.div>
        {teamLogos && <FloatingImage src={teamLogos.SA} alt="team_logo" />}
      </div>
    );
  }
};

type InputContainerProps = {
  label: string;
  children: React.ReactNode;
  id: string;
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

const ChooseTeamManually = () => {
  // Choose team manually using react-select
  const cricketTeams = [
    { value: "india", label: "India" },
    { value: "australia", label: "Australia" },
    { value: "england", label: "England" },
    { value: "south_africa", label: "South Africa" },
  ];

  const players = [
    { value: "player1", label: "Player 1" },
    { value: "player2", label: "Player 2" },
    { value: "player3", label: "Player 3" },
    { value: "player4", label: "Player 4" },
    { value: "player5", label: "Player 5" },
    { value: "player6", label: "Player 6" },
    { value: "player7", label: "Player 7" },
    { value: "player8", label: "Player 8" },
    { value: "player9", label: "Player 9" },
    { value: "player10", label: "Player 10" },
  ];
  return (
    <div className="flex-center flex-col">
      <motion.div animate={{}} className="top-container">
        <FloatingImage first src="/mi.png" alt="team_logo" />
        <div className="inputs-container">
          <InputContainer label="Choose Team 1" id="team1">
            <CustomSelect/>
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
      <div className="btn-cont">
        <AnimatedButton disabled={false} />
      </div>
    </div>
  );
};

interface FloatingImageProps {
  src: string;
  alt: string;
  width?: number;
  first?: boolean;
}

const FloatingImage: React.FC<FloatingImageProps> = ({
  src,
  alt,
  width = 250,
  first = false,
}) => {
  // Variants for entry + floating animations
  const entryAndFloat = {
    hidden: (first: boolean) => ({
      opacity: 0,
      x: first ? 100 : -100, // First image slides in from right, others from left
    }),
    visible: {
      opacity: 1,
      x: 0,
      transition: {
        duration: 1, // Entry animation duration
        ease: "easeInOut",
      },
    },
    floating: {
      y: [-10, 0, -10], // Floating up and down
      rotate: [-1, 0, -1], // Subtle rotation
      transition: {
        duration: 5, // Floating animation duration
        ease: "easeInOut",
        repeat: Infinity, // Infinite repeat
      },
    },
  };

  return (
    <motion.img
      src={src}
      alt={alt}
      width={width}
      custom={first} // Pass `first` dynamically
      initial="hidden"
      animate={["visible", "floating"]} // First, perform entry; then, start floating
      variants={entryAndFloat}
      className="select-team-img"
      style={{
        width: width,
        height: "auto",
      }}
    />
  );
};

const AnimatedButton = ({ disabled }: { disabled: boolean }) => {
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
        boxShadow: disabled ? "" : "-5px 5px 40px #ff5d6b",
        background: "#ff4141",
        color: disabled ? "rgba(255, 255, 255, 0.5)" : "rgba(255, 255, 255)",
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
      disabled={disabled}
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
      <AutoAwesomeIcon style={{ fontSize: 30 }} />
      Generate your Dream Team
    </motion.button>
  );
};

export default ChooseTeam;
