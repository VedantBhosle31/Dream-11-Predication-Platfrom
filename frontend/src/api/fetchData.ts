import { useState } from "react";


// export const fetchData = async <T>(url: string): Promise<T> => {
//     const response = await fetch(url);
  
//     if (!response.ok) {
//       throw new Error(`Error: ${response.statusText}`);
//     }
  
//     const data: T = await response.json();

//     console.log(response);

//     return data;
    
//   };
  

//   const [numbers, setNumbers] = useState<number[]>([]);

//   export const fetchData = async (): Promise<> => {
//     const response = await fetch(
//       "http://127.0.0.1:8000/graphs/get_player_radar_chart/1/"
//     );
//     if (!response.ok) {
//       throw new Error("Failed to fetch data");
//     }
//     console.log("response", response);

//     const jsonData = await response.json();

//     // Extracting only values from the JSON
//     const values = Object.values(jsonData) as number[];

//     // setNumbers(values);

//     return jsonData;
//   };


// export const fetchData = async <T>(url: string): Promise<T> => {
//     const response = await fetch(url);
  
//     if (!response.ok) {
//       throw new Error(`Error: ${response.statusText}`);
//     }

//     console.log("response",response);
  
//     const data: T = await response.json();
//     return data;
//   };
  

export type BackendData = {
    Date: string; // ISO date string
    Previous_Runs: number; // Run count
  };
  
  export const fetchData = async (url: string): Promise<BackendData[]> => {
    const response = await fetch(url);
  
    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }
  
    const data: BackendData[] = await response.json();
    return data;
  };
  