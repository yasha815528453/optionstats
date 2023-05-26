import { ColorModeContext, useMode} from './theme';
import { CssBaseline, ThemeProvider } from '@mui/material';
import { Routes, Route } from "react-router-dom"
import Rankings from "./scenes/rankings"
import Overview from "./scenes/overview"
import Topbar from './scenes/global/topbar';
import Sidebar from "./scenes/global/sidebar"
import Disclaimer from './scenes/global/disclaimer';
import Sectors from "./scenes/sectors"
import Expectationschart from './scenes/expectation';
import Faq from './scenes/faq';
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
            <Route path="/" element={<Overview />} />
            <Route path="/rankings" element={<Rankings />} />
            <Route path="/sectorranking" element={<Sectors />} />
            <Route path="/expectations" element={<Expectationschart />} />
            <Route path="/FAQ" element={<Faq />} />
          </Routes>
          <Disclaimer />
        </main>
      </div>
    </ThemeProvider>

  </ColorModeContext.Provider>
  );
}

export default App;
