import React,{useEffect, useState} from "react";
import { queryChats } from "../api/api";

function BottomInput({disabled, onAdd, sources, onAnswer}){
    const [query,setQuery] = useState("");

    const handleSend = async()=> {
        if(!query.trim()) return;

        try{
            const activeSources = sources.filter(s=>s.active).map(s=>s.source_id);
            console.log("activeSources", activeSources);
            const result = await queryChats(query, activeSources);

            // console.log(result);
            // console.log("sending to chat", result.answer);

            onAnswer({
                question: query,
                answer: result.answer.answer,
                chunks: result.retrieved_chunks
            });

            setQuery("");
        } catch (err) {
            console.error(err);
        }
    }

    return(
        <div className="bottom-input">
            <button className="add-btn" onClick={onAdd} disabled={disabled}>+</button>

            <div className="input-wrapper">
                <input
                    type ="text"
                    placeholder="Ask something..."
                    disabled={disabled}
                    value={query}
                    onChange={(e)=> setQuery(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") handleSend();
                    }}
                />
            </div>
            <button className="send-btn" disabled={disabled} onClick={handleSend}>Send</button>
        </div>
    );
}

export default BottomInput;