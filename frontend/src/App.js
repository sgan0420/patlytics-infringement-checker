import { useState } from "react";
import logo from "./logo.svg";
import "./App.css";

const App = () => {
  const [patentId, setPatentId] = useState("");
  const [companyName, setCompanyName] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Form Submitted", { patentId, companyName });

    // Example: Sending the data to the backend (implement in Step 3)
    // sendToBackend({ patentId, companyName });
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} alt="Patlytics Logo" style={{ width: "200px" }} />
      </header>
      <main className="App-main">
        <form className="App-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="patentId">Patent ID:</label>
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
            <label htmlFor="companyName">Company Name:</label>
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
      </main>
    </div>
  );
};

export default App;
