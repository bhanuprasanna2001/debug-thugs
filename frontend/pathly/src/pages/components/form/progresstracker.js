import React, { useEffect, useState } from "react";
import axios from "axios";

const ProgressTracker = ({ userId }) => {
  const [progress, setProgress] = useState(null);

  useEffect(() => {
    if (!userId) return;
    axios.get(`http://localhost:5000/api/user-progress/${userId}`)
      .then(res => setProgress(res.data))
      .catch(err => console.error("Progress error:", err));
  }, [userId]);

  if (!progress) return null;

  return (
    <div className="mt-4 mb-5">
      <h5>📈 Your Course Progress</h5>
      <div className="progress" style={{ height: "20px" }}>
        <div
          className="progress-bar bg-success"
          role="progressbar"
          style={{ width: `${progress.percent}%` }}
          aria-valuenow={progress.percent}
          aria-valuemin="0"
          aria-valuemax="100"
        >
          {progress.percent}%
        </div>
      </div>
      <p className="text-muted mt-2">{progress.completed} out of {progress.total} days completed</p>
    </div>
  );
};

export default ProgressTracker;