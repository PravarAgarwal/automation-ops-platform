import React, { useEffect, useState } from "react";
import { http } from "./api/client";

export default function App() {
  const [message, setMessage] = useState("Checking backend...");

  useEffect(() => {
    http
      .get("/health")
      .then((res) => setMessage(JSON.stringify(res.data)))
      .catch((err) => setMessage(err.message));
  }, []);

  return (
    <div style={{ padding: 40, fontSize: 18 }}>
      <h1 style={{ fontSize: 24 }}>Frontend ↔ Backend Test</h1>
      <p>{message}</p>
    </div>
  );
}
