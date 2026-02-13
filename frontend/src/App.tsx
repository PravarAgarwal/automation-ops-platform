import React, { useEffect, useState } from "react";
import { listJobs } from "./api/jobs";
import type { Job } from "./types/job";

export default function App() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [message, setMessage] = useState("Loading jobs...");

  useEffect(() => {
    listJobs()
      .then((data) => {
        setJobs(data);
        setMessage(`Loaded ${data.length} job(s)`);
      })
      .catch((err) => setMessage(err.message));
  }, []);

  return (
    <div style={{ padding: 40, fontSize: 18 }}>
      <h1 style={{ fontSize: 24 }}>Jobs (Test)</h1>
      <p>{message}</p>

      <ul>
        {jobs.map((j) => (
          <li key={j.id}>
            #{j.id} — {j.name} ({j.script_type})
          </li>
        ))}
      </ul>
    </div>
  );
}
