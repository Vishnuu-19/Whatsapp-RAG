import React from "react";

function ChatWindow({ messages }) {

  return (
    <div className="chat-window">

      {messages.map((msg, i) => (

        <div key={i} className={`msg ${msg.type}`}>
          {msg.text}
        </div>

      ))}

    </div>
  );
}

export default ChatWindow;