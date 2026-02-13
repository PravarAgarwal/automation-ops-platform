import { http } from "./client";
import type { Job } from "../types/job";

export async function listJobs(): Promise<Job[]> {
  const res = await http.get<Job[]>("/jobs");
  return res.data;
}