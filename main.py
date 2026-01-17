import pandas as pd
from ingestion.preprocessing import parse_whatsapp_chat
from ingestion.chunking import create_chunks

if __name__ == "__main__":
    messages = parse_whatsapp_chat(r"data\raw\WhatsApp Chat with Moksaa bday coming.txt")
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
