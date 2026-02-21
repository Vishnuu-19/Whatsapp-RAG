import pandas as pd
from rag.chunking.preprocessing import parse_whatsapp_chat
from rag.chunking.chunking import create_chunks
from rag.ingestion.ingest import main as ingest_main

if __name__ == "__main__":
    # messages = parse_whatsapp_chat(r"data\raw\WhatsApp Chat with Moksaa bday coming.txt")
    messages = parse_whatsapp_chat(r"data\raw\chat.txt")
    df = pd.DataFrame(messages)
    print("Number of messages: ",len(df))

    chunks = create_chunks(messages)

    # Validation code
    df = pd.DataFrame(chunks)
    print("Number of chunks: ",len(df))

    # print(df[df["sender_id"]=="user_001"].shape[0])
    # print(df[df["is_multiline"] == True][["message_id", "raw_lines_count"]])
    # print(df["raw_lines_count"].value_counts())
    # print(df[df["is_system"]].shape[0])

    print("\nStarting ingestion...")
    ingest_main()
    print("\nCompleted ingestion")
