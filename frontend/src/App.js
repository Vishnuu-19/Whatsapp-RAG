import React,{useEffect,useState} from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import BottomInput from "./components/BottomInput";
import UploadOverlay from "./components/UploadOverlay";
import ConfirmModal from "./components/ConfirmModal";
import { getSources } from "./api/api";
import "./App.css";

function App() {
  const [files, setSources] = useState([]);
  const [messages, setMessages] = useState([]);
  const [isIngesting, setIsIngesting] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(null);

  useEffect(() => {
    loadSources();
  }, []);

  const loadSources = async () => {
    const res = await getSources();
    setSources(res);
  };

  return (
    <div className="app-container">
      <Sidebar
        files={files}
        setConfirmDelete={setConfirmDelete}
        reload={loadSources}
      />

      <div className="main-area">
        <ChatWindow messages={messages} />

        <BottomInput
          disabled={isIngesting}
          onAdd={() => setShowUpload(true)}
          sources = {files}
          onAnswer={(msg) => {
            setMessages((prev) => [
              ...prev,
              { type: "user", text: msg.question },
              { type: "bot", text: msg.answer },
            ]);
          }}
        />
      </div>

      {showUpload && (
        <UploadOverlay
          onClose={() => setShowUpload(false)}
          setIsIngesting={setIsIngesting}
          reload={loadSources}
        />
      )}

      {confirmDelete && (
        <ConfirmModal
          file={confirmDelete}
          onClose={() => setConfirmDelete(null)}
          reload={loadSources}
        />
      )}
    </div>
  );
}

export default App;
