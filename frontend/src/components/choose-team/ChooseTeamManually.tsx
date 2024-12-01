import { motion } from "framer-motion";
import CustomSelect from "./MultiSelect";
import { AnimatedButton, FloatingImage, InputContainer } from "./ChooseTeam";
import { useCallback, useEffect, useState } from "react";
import { debounce } from "lodash";

const ChooseTeamManually = () => {
  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");
  const [players, setPlayers] = useState([]);
  const [matchDate, setMatchDate] = useState("");
  const [apiTeams, setApiTeams] = useState<string[]>([]);
  const [apiPlayers, setApiPlayers] = useState<string[]>([]);

  console.log(players);

  const fetchTeams = useCallback(
    debounce(async (input: string) => {
      if (input.trim().length > 3) {
        const response = await fetch(
          `http://localhost:8000/players/get-teams?user_input=${input}`
        );
        const data = await response.json();
        if (data.team_names) {
          setApiTeams(
            data.team_names.map((team: string) => ({
              value: team,
              label: team,
            }))
          );
        }
      }
    }, 500),
    []
  );

  const fetchPlayers = useCallback(
    debounce(async (input: string) => {
      if (input.trim().length > 3) {
        const response = await fetch(
          `http://localhost:8000/players/get-players?user_input=${input}`
        );
        const data = await response.json();
        if (data.player_names) {
          setApiPlayers(
            data.player_names.map((player: string) => ({
              value: player,
              label: player,
            }))
          );
        }
      }
    }, 500),
    []
  );

  const handleTeamInputChange = (inputValue: string) => {
    fetchTeams(inputValue);
  };

  const handlePlayerInputChange = (inputValue: string) => {
    fetchPlayers(inputValue);
  };

  return (
    <div className="flex-center flex-col">
      <motion.div animate={{}} className="top-container gap-x-10">
        <FloatingImage first src="/mi.png" alt="team_logo" />
        <div className="inputs-container">
          <div className="flex gap-4 w-[500px] justify-between">
            <CustomSelect
              data={apiTeams}
              isMulti={false}
              label="Team 1"
              placeholder="Select Team 1"
              widthString="w-[240px]"
              onChange={(inputValue) => setTeam1(inputValue.value)}
              onInputChange={handleTeamInputChange}
            />
            <CustomSelect
              data={apiTeams}
              isMulti={false}
              label="Team 2"
              placeholder="Select Team 2"
              widthString="w-[240px]"
              onChange={(inputValue) => setTeam2(inputValue.value)}
              onInputChange={handleTeamInputChange}
            />
          </div>

          <CustomSelect
            data={apiPlayers}
            isMulti={true}
            label="Select Players"
            placeholder="Select Players"
            widthString="w-[500px]"
            onChange={(inputValue) =>
              setPlayers(inputValue.map((player: any) => player.value))
            }
            onInputChange={handlePlayerInputChange}
          />

          <InputContainer label="Choose Match Date" id="matchDate">
            <input
              value={matchDate}
              onChange={(e) => setMatchDate(e.target.value)}
              type="date"
              style={{ width: 500 }}
              className="px-2"
            />
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

export default ChooseTeamManually;
