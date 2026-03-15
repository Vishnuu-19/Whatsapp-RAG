import axios from "axios";

const baseURL = "http://127.0.0.1:8000"


// export const getFiles = () => API.get("/files");
// export const uploadFiles = (formData) => API.post("/files.upload", formData);
// export const startIngestion = (fileId) => API.post(`/files/${fileId}/ingest`);
// export const pauseFile = (fileId) => API.patch(`/files/${fileId}/pause`);
// export const activateFile = (fileId) => API.patch(`/files/${fileId}/activate`);
// export const deleteFile = (fileId) => API.delete(`/files/${fileId}`);
// export const queryRAG = (query) => API.post("/query", {query});

export async function uploadChats(files){
    const formData = new FormData();

    for(let file of files){
        formData.append("files", file);
    }

    const res = await fetch(`${baseURL}/ingest/`, {
        method:"POST",
        body: formData,
    });

    return res.json();
}

export async function queryChats(question, sources){
    const res = await fetch(`${baseURL}/query/`, {
        method:"POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            question: question,
            sources: sources,
        }),
    });
    return res.json();
}

export async function getSources(){
    const res = await fetch(`${baseURL}/sources/`);
    return res.json();
}

export async function deactivateSource(source_id){
    const res = await fetch(`${baseURL}/sources/${source_id}/deactivate`, {
        method:"POST",
    });
    return res.json();
}

export async function reactivateSource(source_id){
    const res = await fetch(`${baseURL}/sources/${source_id}/reactivate`, {
        method:"POST",
    });
    return res.json();
}

export async function deleteSource(source_id) {
    const res = await fetch(`${baseURL}/sources/${source_id}`, {
        method: "DELETE",
    });
    return res.json();
}