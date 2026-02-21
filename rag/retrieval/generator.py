import subprocess
import json

class AnswerGenerator:
    def __init__(self, model_name = "llama3.1:8b"):
        self.model_name = model_name

    def build_prompt(self, user_query: str, retrieved_chunks: list):
        context_block = "\n\n".join(
            [f"[Chunks{i+1} | Sender:{c['sender_id']}]\n{c['text']}" for i,c in enumerate(retrieved_chunks)]
        )

        prompt = f"""
            You are answering a question using ONLY the provided WhatsApp chat excerpts.

            Rules:
            - Use only the provided chunks.
            - Do NOT add information not present.
            - If answer is not found, say "No relevant information found."
            - Preserve attribution (who said what).

            Question:
            {user_query}

            Chat Excerpts:
            {context_block}

            Answer:
        """

        return prompt.strip()
    
    def generate(self, user_query: str, retrieved_chunks: list):
        if not retrieved_chunks:
            return "No relevant chunks found."

        prompt = self.build_prompt(user_query, retrieved_chunks)

        process = subprocess.Popen(
            ["ollama", "run", self.model_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        output, error = process.communicate(prompt)

        if process.returncode != 0:
            raise RuntimeError(f"Ollama error: {error}")
        
        return output.strip()