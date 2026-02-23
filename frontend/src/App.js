import React,{useEffect,useState} from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import BottomInput from "./components/BottonInput";
import UploadOverlay from "./components/UploadOverlay";
import ConfirmModal from "./components/ConfirmModal";
import { getFiles } from "./api/api";
import "./App.css";

function App() {
  const [files, setFiles] = useState([]);
  const [isIngesting, setIsIngesting] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(null);

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    const res = await getFiles();
    setFiles(res.data);
  };

  return (
    <div className="app-container">
      <Sidebar
        files={files}
        setConfirmDelete={setConfirmDelete}
        reload={loadFiles}
      />

      <div className="main-area">
        {isIngesting && <UploadOverlay />}
        <ChatWindow isDisabled={isIngesting} />

        <BottomInput
          disabled={isIngesting}
          onAdd={() => setShowUpload(true)}
        />
      </div>

      {showUpload && (
        <UploadOverlay
          onClose={() => setShowUpload(false)}
          setIsIngesting={setIsIngesting}
          reload={loadFiles}
        />
      )}

      {confirmDelete && (
        <ConfirmModal
          file={confirmDelete}
          onClose={() => setConfirmDelete(null)}
          reload={loadFiles}
        />
      )}
    </div>
  );
}

export default App;
