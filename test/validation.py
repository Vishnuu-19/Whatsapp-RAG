import pandas as pd
from preprocessing import parse_whatsapp_chat, write_messages_json

if __name__ == "__main__":
    messages = parse_whatsapp_chat(r"C:\Users\vishn\OneDrive\Desktop\Whatsapp-RAG\data\raw\_chat.txt")
    
    df = pd.DataFrame(messages)

    print(df[df["sender_id"]=="user_001"].shape[0])
    print(df[df["is_multiline"] == True][["message_id", "raw_lines_count"]])
    print(df["raw_lines_count"].value_counts())

    
    
