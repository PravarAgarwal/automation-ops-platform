import axios from "axios";

const baseURL = "http://127.0.0.1:8000";

export const http = axios.create({
  baseURL,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
  }
});