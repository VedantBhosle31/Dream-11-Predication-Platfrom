from dotenv import load_dotenv
import os
from groq import Groq

from players.utils.player_service import get_player_stats
from .templates import select_template, adapt_template, implement_template, batter_reasoning_modules, bowler_reasoning_modules, video_gen_solve_template

# Load environment variables from .env
load_dotenv()

# Use API key from environment
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
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

# CHECK ROLE FROM PLAYER DATA
def self_discover(user_task, player_data):
  # if batter or bowler or all-rounder or wicket-keeper choose the relevant modules
  select_prompt = select_template.format(user_task, batter_reasoning_modules)
  selected_modules = generate_completion(select_prompt)
  print('Selected Modules:', selected_modules.content)

  adapt_prompt = adapt_template.format(user_task, selected_modules)
  adapted_modules = generate_completion(adapt_prompt)
  print("Adapted Modules:",adapted_modules.content)

  implement_prompt = adapt_template.format(user_task, adapted_modules)
  implemented_schema = generate_completion(implement_prompt)
  print("Implemented schema:", implemented_schema.content)

  return implemented_schema

def solve_task(user_task, relevant_convos, implemented_schema):
  prompt = video_gen_solve_template.format(user_task, relevant_convos, implemented_schema)
  answer = generate_completion(prompt)
  return answer

user_task = '''Given the stats of a player, give a commentary with deep insights. Keep it under 200 words.'''

# Pick the json depending on player type (batter/bowler/wk/all-rounder)
def get_explainable_data(name, match_date, format, player_type):
  print('in get scripts')
  data = get_player_stats(name, match_date, format)
  print(data)
  # player_data_json = data[player_type]
  player_data_json = {}
  implemented_schema = self_discover(user_task, player_data_json)
  answer = solve_task(user_task, player_data_json, implemented_schema)

  return answer

# GOT