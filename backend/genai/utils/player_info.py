from groq_client import generate_completion


def player_description(player_json,feature_name,user_task=''):
    # Reasoning modules
  batter_reasoning_modules = [
      "Matchup Analysis",
      "Venue Performance",
      "Form Evaluation",
      "Consistency Assessment",
      "Impact Analysis",
      "Boundary Hitting",
      "Pressure Performance",
      "Opposition Analysis",
      "Strike Rotation",
      "Clutch Scoring"
  ]
  bowler_reasoning_modules = [
      "Matchup Analysis",
      "Venue Effectiveness",
      "Form and Wicket-Taking Ability",
      "Economy and Control",
      "Pressure Bowling",
      "Adaptability",
      "Boundary Containment",
      "Impactful Overs",
      "Bowler-Batter Plans",
      "Supportive Role"
  ]
  select_template = '''Select several reasoning modules that are crucial to utilize in order to solve the given task

  ---

  Follow the following format.

  User Task: {}
  Modules: Available reasoning modules to solve given user task : {}
  Selected Modules: Select several modules that are crucial for solving the tasks above

  ---
  '''

  adapt_template = '''Rephrase and specify each reasoning module so that it better helps solving the task

  ---

  Follow the following format.

  User Task: {}
  Selected Modules: {}
  Adapted Modules: Adapt each reasoning module description to better solve the tasks

  ---'''

  implement_template = '''Operationalize the reasoning modules into a step-by-step reasoning plan in JSON format

  ---

  Follow the following format.

  User Task: {}
  Adapted Modules: {}
  Implemented Schema: Implement a reasoning structure in JSON format for solvers to follow step-by-step and arrive at correct answers

  ---
  '''

  if feature_name == 'player_description':
    solve_template = '''Follow the reasoning structure to solve the task. Give a detailed analysis like a real cricket commentator. Fill in the following specifically about the task given, given all the player data. Do not simply rephrase the keys. Return only bullet points, nothing else

---

Follow the following format.

User Task: {}

Player data: {}

Reasoning Structure: {}

Answer: Make sure it follows the correct reasoning structure and the final output is just text like a real commentator speaking. Return only the analysis based on the schema given, do not miss anything. Return only 60 words at max containing as much info as possible under bullets, don't add any extra words about generation like 'here is an analysis' or any ai generation jargon, just to the point. Answer in positive points only, nothing negative about the player. Add more stats and less words

---'''
    user_task = '''Given the stats for the player, pick up good and exciting ones, answer in extremely short and concise bullets not exceeding 10-15 words each, max 6 bullets. Do not return anything other than bullets with max 10-15 words of content each. Give only bullets, don't generate anything that is not human'''

  elif feature_name == 'video_generation':
    solve_template = '''Follow the reasoning structure to solve the task. Give a detailed analysis like a real cricket commentator. Fill in the following specifically about the task given, given all the player data. Do not simply rephrase the keys

---

Follow the following format.

User Task: {}

Player data: {}

Reasoning Structure: {}

Answer: Make sure it follows the correct reasoning structure and the final output is just text like a real commentator speaking. Return only the analysis based on the schema given, do not miss anything. Return upto 150 words at max containing as much info as possible, don't add any extra words about generation like 'here is an analysis', just to the point. Answer in positive points only, nothing negative about the player. Give deep insights using the stats. Answer in a paragraph format

---'''
    user_task = '''You are a cricket analyst.Given the stats of a player, give a commentary analyzing the with deep insights. Keep it under 200 words.'''
  elif feature_name == 'query_answering':
    solve_template = '''Follow the reasoning structure to solve the task. Give a detailed analysis like a real cricket commentator. Fill in the following specifically about the task given, given all the player data. Do not simply rephrase the keys

---

Follow the following format.

User Task: {}

Player data: {}

Reasoning Structure: {}

Answer: Make sure it follows the correct reasoning structure and the final output is just text like a real commentator speaking. Return only the analysis based on the schema given, do not miss anything. Return only 60 words at max containing as much info as possible, don't add any extra words about generation like 'here is an analysis', just to the point. Answer in positive points only, nothing negative about the player. Add more stats and less words
Return string type only.
---'''

  select_prompt = select_template.format(user_task, batter_reasoning_modules)
  selected_modules = generate_completion(select_prompt)

  adapt_prompt = adapt_template.format(user_task, selected_modules)
  adapted_modules = generate_completion(adapt_prompt)

  implement_prompt = adapt_template.format(user_task, adapted_modules)
  implemented_schema = generate_completion(implement_prompt)

  prompt = solve_template.format(user_task, player_json, implemented_schema)
  answer = generate_completion(prompt)



  return answer