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

video_gen_solve_template = '''Follow the reasoning structure to solve the task. Give a detailed analysis like a real cricket commentator. Fill in the following specifically about the task given, given all the player data. Do not simply rephrase the keys

---

Follow the following format.

User Task: {}

Player data: {}

Reasoning Structure: {}

Answer: Make sure it follows the correct reasoning structure and the final output is just text like a real commentator speaking. Return only the analysis based on the schema given, do not miss anything. Return upto 150 words at max containing as much info as possible, don't add any extra words about generation like 'here is an analysis', just to the point. Answer in positive points only, nothing negative about the player. Give deep insights using the stats. Answer in a paragraph format

---'''