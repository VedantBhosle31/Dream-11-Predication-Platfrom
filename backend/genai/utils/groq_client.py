from groq import Groq
import os
from gtts import gTTS

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def generate_completion(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    if hasattr(chat_completion, 'content'):
        return str(chat_completion.content.strip().replace('\\', ''))
    elif hasattr(chat_completion, 'choices'):
        return str(chat_completion.choices[0].message.content.replace('\\', ''))
    else:
        return str(chat_completion).replace('\\', '')
    
def get_audio(pompt):
    tts = gTTS(text=pompt, lang='en')
    tts.save("audio/audio.mp3")
    return "audio/audio.mp3"
    
