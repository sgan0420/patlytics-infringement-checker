import { useState } from "react";
import logo from "./logo.svg";
import "./App.css";

const App = () => {
  const [patentId, setPatentId] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [results, setResults] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!patentId || !companyName) {
      alert("Please fill in both fields");
      return;
    }

    const formData = { patentId, companyName };
    console.log("Form Data Submitted:", formData);

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
          <button type="submit">Submit</button>
        </form>
        {results && (
          <div className="results">
            <p>Infringement Analysis</p>
            <pre>{JSON.stringify(results, null, 2)}</pre>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
