from openai import OpenAI
from config.config import OPENAI_API_KEY

class LLMAgent:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def process_query(self, query, context):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return None