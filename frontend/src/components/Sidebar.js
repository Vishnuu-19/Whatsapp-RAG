import React from "react";
import FileCard from "./FileCard";

function Sidebar({files, setConfirmDelete, reload}) {
    return(
        <div className="sidebar">
            <h3>Sources</h3>
            {files.map((file)=>(
                <FileCard 
                key={file.source_id} 
                file={file}
                setConfirmDelete={setConfirmDelete}
                reload = {reload}
                />
            ))}
        </div>
    );
}

export default Sidebar;