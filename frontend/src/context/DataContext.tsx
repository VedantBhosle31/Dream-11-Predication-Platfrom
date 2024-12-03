// // import React, { createContext, useContext, useState } from "react";

// // // interface PlayerData {
// // //   stats: {
// // //     batting?: Array<BattingStats>;
// // //     bowling?: Array<BowlingStats>;
// // //     fielding?: Array<FieldingStats>;
// // //   };
// // // }

// // interface BattingStats {
// //   [key: string]: any; // If keys are dynamic or unknown
// //   // Or explicitly define keys if they are known:
// //   // For additional keys
// // }

// // interface BowlingStats {
// //   [key: string]: any; // If keys are dynamic or unknown
// //   // Or explicitly define keys if they are known:
// //   // For additional keys
// // }

// // interface FieldingStats {
// //   [key: string]: any; // If keys are dynamic or unknown
// //   // Or explicitly define keys if they are known:
// //   // For additional keys
// // }


// // interface DataContextType {
// //   playerData: any | null;
// //   setPlayerData: React.Dispatch<React.SetStateAction<any | null>>;
// // }

// // const DataContext = createContext<any | undefined>(undefined);

// // export const DataProvider: React.FC<{ children: React.ReactNode }> = ({
// //   children,
// // }) => {
// //   const [playerData, setPlayerData] = useState<any | null>(null);

// //   return (
// //     <DataContext.Provider value={{ playerData, setPlayerData }}>
// //       {children}
// //     </DataContext.Provider>
// //   );
// // };

// // export const useDataContext = () => {
// //   const context = useContext(DataContext);
// //   if (!context) {
// //     throw new Error("useDataContext must be used within a DataProvider");
// //   }
// //   return context;
// // };






// // import React from 'react';

// // interface UserContextType {
// //   details: any;
// // }

// // export const UserContext = React.createContext<UserContextType | null>(null);



// // export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
// //   const [user] = React.useState<UserContextType>({details:["gvuhjb0"]});

// //   return (
// //     <UserContext.Provider value={user}>
// //       {children}
// //     </UserContext.Provider>
// //   );
// // };



// import React, { useState, useContext } from 'react';

// // interface UserContextType {
// //   details: any;
// //   setDetails: React.Dispatch<React.SetStateAction<any | null>>;
// // }

// interface UserContextType {
//   details: any;
//   setDetails: React.Dispatch<React.SetStateAction<any>>;
// }


// export const UserContext = React.createContext<UserContextType | null>(null);

// export const UserProvider: React.FC<{ children: JSX.Element}> = ({ children }) => {
//   const [details, setDetails] = useState<any>([]);

//   return (
//     <UserContext.Provider value={{ details, setDetails }}>
//       {children}
//     </UserContext.Provider>
//   );
// };

// // Custom hook for easier access to the context
// export const useUserContext = () => {
//   const context = useContext(UserContext);
//   if (!context) {
//     throw new Error("useUserContext must be used within a UserProvider");
//   }
//   return context;
// };
export {}