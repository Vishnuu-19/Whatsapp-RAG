import React from "react";
import {deactivateSource, reactivateSource} from "../api/api";

function FileCard({file, setConfirmDelete, reload}){
    const togglePause = async() => {
        if(file.active){
            await deactivateSource(file.source_id);
        }else{
            await reactivateSource(file.source_id);
        }
        reload();
    }

    return (
        <div className={`file-card ${file.active ? "paused" : ""}`}>
            <div className="top-right" onClick={togglePause}>
                {file.active ? "⏸" : "▶"}
            </div>

            <div className="file-name">{file.source_id}</div>
            <div className="status">Chunks: {file.chunk_count}</div>

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