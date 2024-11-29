export const setSessionData = <T>(key: string, value: T): void => {
    sessionStorage.setItem(key, JSON.stringify(value));
  };
  
  export const getSessionData = <T>(key: string): T | null => {
    const data = sessionStorage.getItem(key);
    return data ? (JSON.parse(data) as T) : null;
  };
  
  export const clearSessionData = (key: string): void => {
    sessionStorage.removeItem(key);
  };
  