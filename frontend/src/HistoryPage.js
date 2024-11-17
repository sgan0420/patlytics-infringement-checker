import { useState, useEffect } from "react";

const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:5000";

const HistoryPage = () => {
  const [history, setHistory] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(`${apiUrl}/api/get-analysis-history`);
        const data = await response.json();
        setHistory(data);
      } catch (error) {
        console.error("Error fetching history:", error);
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="results">
      <p>Analysis History</p>
      {history ? (
        history.length ? (
          history.map((entry) => (
            <div key={entry.analysis_id} className="results-card">
              <pre>{JSON.stringify(entry, null, 2)}</pre>
            </div>
          ))
        ) : (
          <p>No analysis history found.</p>
        )
      ) : (
        <p>Loading history...</p>
      )}
    </div>
  );
};

export default HistoryPage;
