import { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import logo from "./logo.svg";
import "./App.css";
import HistoryPage from "./HistoryPage";

const App = () => {
  const [patentId, setPatentId] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isAnalysisSaved, setIsAnalysisSaved] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const onAnalyse = async (e) => {
    e.preventDefault();

    if (!patentId || !companyName) {
      setErrorMessage("Please fill in both input fields");
      return;
    }

    const formData = { patentId, companyName };
    console.log("Form Data Submitted:", formData);

    setLoading(true);
    setIsAnalysisSaved(false);
    setErrorMessage("");

    try {
      const response = await fetch(
        "http://backend:5000/api/analyze-patent-infringement",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
        }
      );
      const data = await response.json();
      console.log("Response from Backend:", data);
      if (response.ok) {
        setResults(data);
      } else {
        setErrorMessage(
          data.error || "An error occurred while analyzing the patent."
        );
      }
    } catch (error) {
      console.error("Error submitting data:", error);
      setErrorMessage("There was a problem with the request.");
    } finally {
      setLoading(false);
    }
  };

  const onSaveAnalysis = async () => {
    if (!results) return;

    try {
      const response = await fetch("http://backend:5000/api/save-analysis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(results, null, 2),
      });
      const data = await response.json();

      if (response.ok) {
        console.log("Save Analysis Response:", data);
        setIsAnalysisSaved(true);
        setErrorMessage("");
      } else {
        setErrorMessage(data.error || "Failed to save the analysis.");
      }
    } catch (error) {
      console.error("Error saving analysis:", error);
      setErrorMessage("There was a problem saving the analysis.");
    }
  };

  const openHistoryPageInNewTab = () => {
    window.open("/history", "_blank");
  };

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <img src={logo} alt="Patlytics Logo" style={{ width: "200px" }} />
        </header>
        <main className="App-main">
          <Routes>
            <Route
              path="/"
              element={
                <>
                  <form className="App-form" onSubmit={onAnalyse}>
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

                  <button
                    onClick={openHistoryPageInNewTab}
                    className="button-dark"
                  >
                    View History <span className="arrow">&#8599;</span>
                  </button>

                  {errorMessage && (
                    <div className="error-message">
                      <p>{errorMessage}</p>
                    </div>
                  )}

                  {results && !loading && (
                    <div className="results">
                      <p>Infringement Analysis</p>
                      <div className="results-card">
                        {!results["error"] && (
                          <button
                            className="button-dark"
                            onClick={onSaveAnalysis}
                            disabled={isAnalysisSaved}
                          >
                            {isAnalysisSaved ? (
                              <span className="done-icon">Saved ✔</span>
                            ) : (
                              "Save Analysis"
                            )}
                          </button>
                        )}
                        <pre>{JSON.stringify(results, null, 2)}</pre>
                      </div>
                    </div>
                  )}
                </>
              }
            />
          </Routes>
          <Routes>
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
