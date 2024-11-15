import { useState } from "react";
import logo from "./logo.svg";
import "./App.css";

const App = () => {
  const [patentId, setPatentId] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState(null);
  const [saveStatus, setSaveStatus] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!patentId || !companyName) {
      alert("Please fill in both fields");
      return;
    }

    const formData = { patentId, companyName };
    console.log("Form Data Submitted:", formData);

    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/infringement-check",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
        }
      );
      const data = await response.json();
      console.log("Response from Backend:", data);
      setResults(data);
    } catch (error) {
      console.error("Error submitting data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveAnalysis = async () => {
    if (!results) return;

    try {
      const response = await fetch("http://127.0.0.1:5000/api/save-analysis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(results),
      });
      const data = await response.json();
      console.log("Save Analysis Response:", data);
      setSaveStatus("Analysis saved successfully!");
    } catch (error) {
      console.error("Error saving analysis:", error);
      setSaveStatus("Failed to save analysis.");
    }
  };

  const handleViewHistory = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/analysis-history",
        {
          method: "GET",
        }
      );
      const data = await response.json();
      console.log("History from Backend:", data);
      setHistory(data);
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} alt="Patlytics Logo" style={{ width: "200px" }} />
      </header>
      <main className="App-main">
        <form className="App-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="patentId">Patent ID</label>
            <input
              type="text"
              id="patentId"
              name="patentId"
              placeholder="Enter Patent ID"
              value={patentId}
              onChange={(e) => setPatentId(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="companyName">Company Name</label>
            <input
              type="text"
              id="companyName"
              name="companyName"
              placeholder="Enter Company Name"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? "Loading..." : "Analyse"}
          </button>
        </form>
        <button className="button-dark" onClick={handleViewHistory}>
          View History
        </button>
        {results && (
          <div className="results">
            <p>Infringement Analysiss</p>
            <div className="results-card">
              <pre>{JSON.stringify(results, null, 2)}</pre>
              <button className="button-dark" onClick={handleSaveAnalysis}>
                Save Analysis
              </button>
            </div>
          </div>
        )}
        {saveStatus && <p>{saveStatus}</p>}
        {history && (
          <div className="results">
            <p>Analysis History</p>
            <pre>{JSON.stringify(history, null, 2)}</pre>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
