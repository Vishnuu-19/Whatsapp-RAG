import React from "react";
import { deleteFile } from "../api/api";

function ConfirmModal({file, onClose, reload}){
    const handleDelete = async()=>{
        await deleteFile(file.file_id);
        reload();
        onClose();
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <h3>Delete {file.filename}</h3>
                <button onClick={onclose}>Cancel</button>
                <button onClick={handleDelete}>Delete</button>
            </div>
        </div>
    );
}

export default ConfirmModal;