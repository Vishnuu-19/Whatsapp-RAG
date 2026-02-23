import React from "react";
import {pauseFile, activateFile} from "../api/api";

function FileCard({file, setConfirmDelete, reload}){
    const togglePause = async() => {
        if(file.active){
            await pauseFile(file.file_id);
        }else{
            await activateFile(file.file_id)
        }
        reload();
    }

    return (
        <div className={`file-card ${file.active ? "paused" : ""}`}>
            <div className="top-right" onClick={togglePause}>
                {file.active ? "⏸" : "▶"}
            </div>

            <div className="file-name">{file.filename}</div>
            <div className="status">Status: {file.status}</div>

            <div
                className="bottom-right"
                onClick={() => setConfirmDelete(file)}
            >
                🗑
            </div>
        </div>
    );
}

export default FileCard;