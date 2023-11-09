import * as React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { createTheme, ThemeProvider } from "@mui/material/styles";
import MyToolBar from './MyToolBar';
export default function App() {
  const theme = createTheme({
    palette: {
      mode: 'light',
      primary: {
        main: '#334192',
      },
      secondary: {
        main: '#f50057',
      },
    }, 
  });
  return (
    <ThemeProvider theme={theme}>
    <Router>
    <MyToolBar />
    </Router>   
    </ThemeProvider>
  );
}