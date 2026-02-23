import React,{useEffect, useState} from "react";

function BottomInput({disabled, onAdd}){
    const [query,setQuery] = useState("");

    return(
        <div className="bottom-input">
            <button onClick={onAdd}>+</button>

            <input
                type ="text"
                placeholder="Ask something..."
                disabled={disabled}
                value={query}
                onChange={(e)=> setQuery(e.target.value)}
            />
            <button disabled={disabled}>Send</button>
        </div>
    );
}

export default BottomInput;