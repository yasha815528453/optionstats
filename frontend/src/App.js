import { ColorModeContext, useMode} from './theme';
import { CssBaseline, ThemeProvider } from '@mui/material';
import { Routes, Route } from "react-router-dom"
import Overview from "./scenes/overview"
import Topbar from './scenes/global/topbar';
import Sidebar from "./scenes/global/sidebar"
// import winners from "./scenes/winners"
// import insights from "./scenes/insights"
// import charting from "./scenes/charting" // maybe dont need? idk.. can expand



function App() {
  const [theme, colorMode] = useMode();

  return (
  <ColorModeContext.Provider value={colorMode}>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app">
        <Sidebar />
        <main className="content">
          <Topbar />
          <Routes>
            {/* <Route path="/" element={<Overview />} /> */}
            {/* <Route path="/winners" element={<winners />} />
            <Route path="/insights" element={<insights />} /> */}
            {/* maybe more can be added later.. */}
          </Routes>
        </main>
      </div>
    </ThemeProvider>

  </ColorModeContext.Provider>
  );
}

export default App;
