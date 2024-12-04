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
    
get_audio("What a thrilling prospect! We're diving into the statistics of this exceptional batsman, and I'm excited to share the findings with you, dear viewers!\n\nThis batsman has been in exceptional form of late, showcasing impressive consistency. They've notched three half-centuries in their last five innings, with a remarkable fifties percentage of 60%. Their century rate has also been on the rise, with a healthy average of 45.67. It's clear that they're in a rich vein of form, and we can expect them to continue making significant contributions to the team.\n\nMoving on to their venue-specific expertise, it's striking to see the batsman's exceptional record at faster-paced wickets. They've averaged a robust 42.31 and struck at 85.12 against pace-friendly conditions. It's evident that they thrive in these conditions, and their strategic approach is adept at countering the threat of pacey bowlers.")
