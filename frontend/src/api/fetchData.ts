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
  