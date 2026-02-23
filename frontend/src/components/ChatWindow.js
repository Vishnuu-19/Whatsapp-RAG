import React,{useEffect, useState} from "react";
import { queryRAG } from "../api/api";

function ChatWindow({isDisabled}){
    const [messages, setMessages] = useState([]);

    const sendQuery = async(query)=>{
        const res = await queryRAG(query);
        setMessages([
            ...messages,
            { type: "user",text: query},
            { type: "bot", text: res.data.answer },
        ]);
    };

    return (
        <div className = "chat-window">
            {messages.map((msg,i)=>(
                <div key={i} className={`msg ${msg.type}`}>
                    {msg.text}
                    </div>
            ))}
        </div>
    );
}

export default ChatWindow;