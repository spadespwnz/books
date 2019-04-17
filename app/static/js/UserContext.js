import React  from 'react';
export const UserContext = React.createContext({
  loggedIn: false,
  name: "",
  onLogout: () => true,
  onLogin: () => true,
  fetchUserData: () => true,
});
