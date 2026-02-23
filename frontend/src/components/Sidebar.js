import React from "react";
import FileCard from "./FileCard";

function Sidebar({files, setConfirmDelete, reload}) {
    return(
        <div classname="sidebar">
            <h3>Files</h3>
            {files.map((file)=>(
                <FileCard 
                key={file.file_id} 
                file={file}
                setConfirmDelete={setConfirmDelete}
                reload = {reload}
                />
            ))}
        </div>
    );
}

export default Sidebar;