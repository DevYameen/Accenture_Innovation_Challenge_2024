import openai
import os
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_email(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or gpt-4 if available
            messages=[
                {"role": "system", "content": "You are an assistant that generates professional emails."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"Error generating email: {e}")
        return None

# Test prompt
if __name__ == '__main__':
    email_prompt = "Write a follow-up email after a business meeting regarding project updates."
    email_body = generate_email(email_prompt)
    if email_body:
        print("Generated Email:", email_body)


