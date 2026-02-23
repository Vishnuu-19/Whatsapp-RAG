import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000",
})

export const getFiles = () => API.get("/files");
export const uploadFiles = (formData) => API.post("/files.upload", formData);
