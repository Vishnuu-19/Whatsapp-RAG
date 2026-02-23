import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000",
})

export const getFiles = () => API.get("/files");
export const uploadFiles = (formData) => API.post("/files.upload", formData);
export const startIngestion = (fileId) => API.post(`/files/${fileId}/ingest`);
export const pauseFile = (fileId) => API.patch(`/files/${fileId}/pause`);
export const activateFile = (fileId) => API.patch(`/files/${fileId}/activate`);
export const deleteFile = (fileId) => API.delete(`/files/${fileId}`);
export const queryRAG = (query) => API.post("/query", {query});