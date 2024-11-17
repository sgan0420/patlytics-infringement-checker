import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import logo from "./logo.svg";
import "./App.css";
import HomePage from "./HomePage";
import HistoryPage from "./HistoryPage";

const apiUrl = process.env.REACT_APP_API_URL;

const App = () => {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <img src={logo} alt="Patlytics Logo" style={{ width: "200px" }} />
        </header>
        <main className="App-main">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
