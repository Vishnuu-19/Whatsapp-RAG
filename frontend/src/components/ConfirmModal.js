import React from "react";
import { deleteSource } from "../api/api";

function ConfirmModal({file, onClose, reload}){
    const handleDelete = async()=>{
        await deleteSource(file.source_id);
        await reload();
        onClose();
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <h3>Delete {file.source_id}</h3>
                <button onClick={onClose}>Cancel</button>
                <button onClick={handleDelete}>Delete</button>
            </div>
        </div>
    );
}

export default ConfirmModal;