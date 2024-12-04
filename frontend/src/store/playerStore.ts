import { create } from "zustand";

interface PlayerStats {
  [key: string]: Record<string, string>;
}

interface PlayerStore {
  teamLogos: string[] | null;
  playerNames: string[];
  playerStats: PlayerStats[];
  best11Players: string[];
  matchDate: string;
  model: string;
  setTeamLogos: (logos: string[] | null) => void;
  setPlayerNames: (names: string[]) => void;
  fetchBest11: () => Promise<Record<string, number>>;
  setMatchDate: (date: string) => void;
  setModel: (model: string) => void;
}

const usePlayerStore = create<PlayerStore>((set, get) => ({
  teamLogos: null,
  playerNames: [],
  playerStats: [],
  best11Players: [],
  matchDate: "",
  model: "",
  graphData: [],
  setTeamLogos: (logos) => set({ teamLogos: logos }),
  setPlayerNames: (names) => set({ playerNames: names }),
  fetchBest11: async () => {
    const response = await fetch(
      `${process.env.REACT_APP_BACKEND_URL}/model/get_predictions`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          names: get().playerNames,
          date: get().matchDate,
          model: get().model,
        }),
      }
    );

    const data = await response.json();
    console.log("API response:", data);

    if (data.fantasy_points && data.predictions) {
      set({ best11Players: data.fantasy_points });
      set({ playerStats: data.predictions });
    } else {
      console.error("API errors:", data.errors);
    }

    return data.fantasy_points || [];
  },
  setMatchDate: (date) => set({ matchDate: date }),
  setModel: (model) => set({ model: model }),
}));

export default usePlayerStore;
