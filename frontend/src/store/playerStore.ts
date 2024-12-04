// import { create } from "zustand";
// import { persist } from "zustand/middleware";

// interface PlayerStats {
//   [key: string]: Record<string, string>;
// }

// interface PlayerStore {
//   teamLogos: string[] | null;
//   playerNames: string[];
//   playerStats: PlayerStats[];
//   best11Players: string[];
//   matchDate: string;
//   model: string;
//   setTeamLogos: (logos: string[] | null) => void;
//   setPlayerNames: (names: string[]) => void;
//   fetchBest11: () => Promise<Record<string, number>>;
//   setMatchDate: (date: string) => void;
//   setModel: (model: string) => void;

//   // dropzone.tsx
//   allmaindata: any[];
//   setallmaindata: (data: any[]) => void;
// }

// const usePlayerStore = create<PlayerStore>(

//   persist((set, get) => ({
//   teamLogos: null,
//   playerNames: [],
//   playerStats: [],
//   best11Players: [],
//   matchDate: "",
//   model: "",
//   setTeamLogos: (logos) => set({ teamLogos: logos }),
//   setPlayerNames: (names) => set({ playerNames: names }),
//   fetchBest11: async () => {
//     const response = await fetch(
//       `${process.env.REACT_APP_BACKEND_URL}/model/get_predictions`,
//       {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//           names: get().playerNames,
//           date: get().matchDate,
//           model: get().model,
//         }),
//       }
//     );

//     const data = await response.json();
//     console.log("API response:", data);

//     if (data.fantasy_points && data.predictions) {
//       set({ best11Players: data.fantasy_points });
//       set({ playerStats: data.predictions });
//     } else {
//       console.error("API errors:", data.errors);
//     }

//     return data.fantasy_points || [];
//   },
//   setMatchDate: (date) => set({ matchDate: date }),
//   setModel: (model) => set({ model: model }),

//   allmaindata: [],
//   setallmaindata: (data) => set({ allmaindata: data }),
// }
// ),{
//   name:"player-store",
//   getStorage: () => localStorage,
// }

// )

// );

// export default usePlayerStore;

import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { CardData } from "../SlidingPanels";

interface PlayerStats {
  [key: string]: Record<string, string>;
}

interface PlayerStore {
  teamLogos: string[] | null;
  playerNames: string[];
  playerStats: PlayerStats[];
  // best11Players: string[];
  best11Players: any[];
  matchDate: string;
  model: string;
  setTeamLogos: (logos: string[] | null) => void;
  setPlayerNames: (names: string[]) => void;
  fetchBest11: () => Promise<Record<string, number>>;
  setMatchDate: (date: string) => void;
  setModel: (model: string) => void;
  allmaindata: any[];
  setallmaindata: (data: any[]) => void;

  displayscreencards: CardData[];
  setdisplayscreencards: (data: any[]) => void;

  playerdescription: string;
  setplayerdescription: (date: string) => void;
}

const usePlayerStore = create<PlayerStore>()(
  persist(
    (set, get) => ({
      teamLogos: null,
      playerNames: [],
      playerStats: [],
      best11Players: [],
      matchDate: "",
      model: "",
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


          // // Transform data into CardData format
          // const transformedBest11: CardData[] = (data.fantasy_points).map(
          //   (player: { name: string; points: number }, index: number) => {
          //     const stats = data.predictions[player.name] || {};
          //     return {
          //       id: `player-${index + 1}`, // Generate a unique ID
          //       name: player.name,
          //       type: stats.type || "N/A",
          //       team: stats.team || "Unknown",
          //       points: player.points.toString(),
          //       cost: stats.cost || "0",
          //       score: stats.score || "0",
          //       cvc: stats.cvc || "N/A",
          //       runs: stats.runs || "0",
          //       average: stats.average || "0.0",
          //       strike_rate: stats.strike_rate || "0.0",
          //       country: stats.country || "Unknown",
          //     };
          //   }
          // );

          

          // console.log("Transformed Best11 Players:", transformedBest11);
        } else {
          console.error("API errors:", data.errors);
        }

        return data.fantasy_points || [];
      },
      setMatchDate: (date) => set({ matchDate: date }),
      setModel: (model) => set({ model: model }),
      allmaindata: [],
      setallmaindata: (data) => set({ allmaindata: data }),

      displayscreencards: [],
      setdisplayscreencards: (data) => set({ displayscreencards: data }),

      playerdescription: "",
      setplayerdescription: (desc) => set({ playerdescription: desc }),
    }),
    {
      name: "player-store", // Key for storage in localStorage
      storage: createJSONStorage(() => localStorage), // Default storage
    }
  )
);

export default usePlayerStore;
