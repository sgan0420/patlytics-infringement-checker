import { useState, useEffect } from "react";

const HistoryPage = () => {
  const [history, setHistory] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/get-analysis-history"
        );
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
      <div className="results-card">
        {history ? (
          <pre>{JSON.stringify(history, null, 2)}</pre>
        ) : (
          <p>Loading history...</p>
        )}
      </div>
    </div>
  );
};

export default HistoryPage;
