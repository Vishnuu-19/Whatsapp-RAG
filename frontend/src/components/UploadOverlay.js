import React, { useState } from "react";
import { uploadChats } from "../api/api";

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

    // Create a ref to trigger the hidden file input
    const fileInputRef = React.useRef(null);

    const handleZoneClick = () => {
        if(fileInputRef.current) {
            fileInputRef.current.click();
        }
    }

    return (
        <div className="upload-overlay">
            <div className="upload-box">
                {!isProcessing ? (
                    <>
                        <h3>Upload Text Extracts</h3>
                        <div className="drop-zone"
                            onDrop={handleDrop}
                            onDragOver={handleDragOver}
                            onClick={handleZoneClick}
                        >Drag & Drop Files or Click to Browse</div>

                        <input
                            type="file"
                            multiple
                            accept=".txt"
                            onChange={handleFileChange}
                            ref={fileInputRef}
                            style={{ display: "none" }}
                        />

                        {selectedFiles.length > 0 && (
                            <div className="file-preview">
                                <p>Selected Files:</p>
                                <ul>
                                {selectedFiles.map((file, idx) => (
                                    <li key={idx}>{file.name}</li>
                                ))}
                                </ul>
                            </div>
                        )}

                        <div className="modal-actions">
                            <button className="close-btn" onClick={onClose}>
                                Cancel
                            </button>
                            
                            {selectedFiles.length > 0 && (
                                <button onClick={handleStartIngestion}>
                                    Start Ingestion
                                </button>
                            )}
                        </div>
                    </>
                ):(
                    <div className="ingestion-state">
                        <h3>Ingestion in progress...</h3>
                        {/* We removed the Pacman loader. The text communicates the state clearly. */}
                    </div>
                )}
            </div>
        </div>
    );
}

export default UploadOverlay;