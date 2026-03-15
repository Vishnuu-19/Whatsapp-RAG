import React, { useState } from "react";
import { uploadChats } from "../api/api";
import PacmanLoader from "./PacmanLoader";

function UploadOverlay({ onClose, setIsIngesting, reload}){
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [isProcessing, setIsProcessing] = useState(false);

    const handleFileChange = (e) => {
        setSelectedFiles(Array.from(e.target.files));
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setSelectedFiles(Array.from(e.dataTransfer.files));
    };

    const handleDragOver = (e) => {
        e.preventDefault();
    };

    const handleStartIngestion = async() => {
        if(selectedFiles.length === 0) return;

        try{
            setIsProcessing(true);
            setIsIngesting(true);

            await uploadChats(selectedFiles);
            
            await reload()

            setIsIngesting(false);
            onClose();
            
        } catch (error) {
            console.error("ingestion failed.",error);
            setIsIngesting(false);
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className="upload-overlay">
            <div className="upload-box">
                {!isProcessing ? (
                    <>
                        <h3>Upload Text Extracts</h3>
                        <div className="drop-zone"
                            onDrop={handleDrop}
                            onDragOver={handleDragOver}
                        >Drag & Drop Files here</div>

                        <input
                            type="file"
                            multiple
                            accept=".txt"
                            onChange={handleFileChange}
                        />

                        {selectedFiles.length > 0 && (
                            <div className="file-preview">
                                <p>Selected Files:</p>
                                <ul>
                                {selectedFiles.map((file, idx) => (
                                    <li key={idx}>{file.name}</li>
                                ))}
                                </ul>

                                <button onClick={handleStartIngestion}>
                                Start Ingestion
                                </button>
                            </div>
                        )}

                        <button className="close-btn" onClick={onClose}>
                            Cancel
                        </button>
                    </>
                ):(
                    <div className="ingestion-state">
                        <h3>Ingestion in progress...</h3>
                        <PacmanLoader />
                    </div>
                )}
            </div>
        </div>
    );
}

export default UploadOverlay;