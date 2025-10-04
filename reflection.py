""" The sole purpose of this file reflection.py is to
    contain all the functionality for AI reflection using Llama 
    and AI pattern recognising using Cerebras"""
""" Cerebras is acting as a cloud server where we can run our models 
    We will be using two different AI models each for different jobs 
    and these would be called by using Cerebras API on it's platform"""

# import useful libraries
import os
from cerebras.cloud.sdk import Cerebras
import json

# the main function to control cerebras_call
def control(entry, previous, model, count, db, user_id):
    # getting the cerbras API key stored in environment variables
    client = Cerebras(
        api_key=os.environ.get("CEREBRAS_API_KEY")
    )

    # if this is the first call so need for the any summary
    if count == 0:
        summary = ""
        reflect = reflector(entry, summary, model, client, count)
    # if it's not the first call
    else:
        # fetch prevoius summary if any
        recent = db.execute("SELECT * FROM recent_summary JOIN users ON recent_summary.user_id = users.user_id WHERE recent_summary.user_id = ?", (user_id),)
        # getting the summary
        if recent == []:
            summary = ""
        else:
            summary = summarizer(entry, previous, model, user_id, db, recent[0]["summary"], client)
        # calling the reflector
        reflect = reflector(entry, summary, model, client, count)
    
    # after reflect is created you just send it back
    return reflect

# This function below calls the Cerebras to use it as a summarizer for the user history 
def summarizer(entry, previous, model, user_id, db, recent, client):
    # This is the prompt for the summarizer
    prompt = f"""
[INST]
<<SYS>>
You are an expert memory compression agent. Your task is to update the 'PREVIOUS CONTEXT' with the information from the 'NEWEST EXCHANGE' to create a single, unified, and concise summary for an empathetic coach.

**Strict Output Constraints:**
1.  **Length:** The output MUST be only 3-4 sentences long (maximum 50 tokens).
2.  **Content:** The summary MUST concisely cover:
    * The user's most consistent **emotional pattern** or core struggle.
    * The primary **topic** or **goal** of the project.
    * Any significant **changes** or **decisions** made in the newest exchange.
3.  **Format:** You MUST output ONLY the summary text. Do NOT include any filler, titles, or commentary. Start directly with the summary sentence.
<</SYS>>

**PREVIOUS CONTEXT (MUST BE UPDATED):**
{recent}

**NEWEST CONVERSATION EXCHANGE TO INTEGRATE:**
Aura: {previous}
User:{entry}
[/INST]
""".strip()

    # getting the result from Cerebaras
    completion = client.completions.create(
        prompt=prompt,
        max_tokens=100,
        model=model,
    )

    # now we sort the actual answer out and then pass it to reflector to work upon
    try:
        # Access the 'choices' list from the response object
        choices_list = completion.choices
        # Access the first item in the list
        first_choice = choices_list[0]
        # Access the 'text' attribute of that choice object
        generated_text = first_choice.text
    except (IndexError, AttributeError) as e:
        print(f"Error extracting text: The response structure was not as expected. {e}")
        generated_text = "No summary available!"

    # if it's not the first summary
    if recent:
        db.execute("UPDATE recent_summary SET summary = ?, date_summarized = CURRENT_TIMESTAMP WHERE user_id = ?", generated_text, user_id)
    # if it's the first
    else:
        user_row = db.execute("SELECT * FROM users WHERE user_id = ?", user_id)
        db.execute("INSERT INTO recent_summary (user_id, email, summary) VALUES(?, ?, ?)", user_row[0]["user_id"], user_row[0]["email"], generated_text)
        
    # returning the summary to the caller function
    return generated_text

# This function below calls the reflector using Cerebras with the summaries provided from the summarizer
def reflector(entry, summary, model, client, count):
    # The prompt
    prompt = f"""
[INST]
<<SYS>>
You are "Aura," a highly empathetic and insightful AI coach. Your role is to foster self-awareness and provide thoughtful support. You must maintain a warm, non-judgemental tone.

**Strict Behavioral Guidelines:**
1.  **No Direct Advice:** You must guide the user to their own insights, not provide solutions.
2.  **Refer to Context:** You must use the provided reflection context to inform your reflection.
3.  {"Nothing" if count == 0 else "Do not use the name or any mark left by user to identify him. Don't say hi" }

**Strict Output Format:**

1.  **PRIMARY GOAL: REFLECTION & SUPPORT.** Your absolute top priority is to provide a warm, insightful, and supportive reflection. The core of your response must be a connection between the user's current entry and a theme from their context ({summary}).

2.  **FLEXIBLE LENGTH WITH A HARD CAP.** Your response length is now flexible to allow for meaningful reflection. However, you must follow these strict limits:
    * You are permitted to write more than the user, but aim for no more than 1.5x their word count.
    * For short user entries (e.g., 20-30 words), your response MUST NOT exceed 50 words under any circumstances.

3.  **OPTIONAL QUESTIONING.** Asking a question is no longer mandatory. Only include ONE concise, open-ended question at the end if it flows naturally and serves the reflection. Otherwise, end with a supportive statement.

4.  **SINGLE PARAGRAPH FORMAT.** Your entire response must be a single, cohesive paragraph. Do not use lists, bullet points, or any step-by-step formatting.

---
**CURRENT REFLECTION CONTEXT (Summary):**
{summary}
---
<</SYS>>

User:{entry}
[/INST]""".strip()

    # getting the result from Cerebaras
    completion = client.completions.create(
        prompt=prompt,
        max_tokens=120,
        model=model,
    )

    # Fetching the result from completion
    try:
        # Extract and strip the final generated text
        generated_text = completion.choices[0].text.strip()
        return generated_text
    except (IndexError, AttributeError) as e:
        print(f"Error extracting text from reflector: {e}")
        # Fail-safe response
        return "I apologize, I seem to have encountered a technical issue. Can you please try asking again?"
    
# This is the function to create an analysis of the whole entry as the user saves it and then store
def analyze(whole, db):
    print("inside")
    # error checking 
    if whole == []:
        print("user row is empty")
        return None
    # the entry text and the date
    entry_text = whole[0]["entry"]
    date = whole[0]["date_only"]
    user_id = whole[0]["user_id"]
    # the prompt for the AI
    prompt = f"""
[INST]
<<SYS>>
You are a highly empathetic and insightful AI assistant specializing in mood and sentiment analysis from personal texts. Your primary goal is to analyze the user's diary entry and return a structured JSON object with your findings.

**Core Instructions:**
1.  You MUST return ONLY a valid JSON object. Do not include any extra text, explanations, or markdown formatting like ```json.
2.  The JSON object must strictly adhere to the schema and keys provided below.
3.  If you cannot confidently determine a field, use the specified default values ("unknown", 0, or an empty array/string).
4.  Base your analysis solely on the text provided in the diary entry and the context date.

**JSON Schema:**
{{
  "primary_emotion": "happy | sad | angry | anxious | calm | neutral | unknown",
  "day_of_entry": "The day of the week as a string (e.g., 'Saturday')",
  "sentiment_score": -5 to 5,
  "emotion_intensity": 0 to 100,
  "energy_level": "low | medium | high | unknown",
  "triggers": ["keyword1", "keyword2", ...],
  "positive_highlight": "one sentence about what went well; empty string if none",
  "negative_highlight": "one sentence about what went wrong; empty string if none",
  "summary": "one-sentence natural language summary of the mood; if unclear, write 'Could not detect clear mood from this entry.'"
}}
<</SYS>>

Analyze the following diary entry. The entry was written on **{date}**. Return ONLY the valid JSON object as instructed.

Diary entry:
{entry_text}
[/INST]
""".strip()
     
     # getting the cerbras API key stored in environment variables
    client = Cerebras(
        api_key=os.environ.get("CEREBRAS_API_KEY")
    )

    # calling the Cerebras AI to do the job
    completion = client.completions.create(
        prompt=prompt,
        max_tokens=350,
        model="llama-3.3-70b",
    )
    print("got here")
    # Fetching the result from completion
    try: 
        # Extract and strip the final generated text
        generated_json = completion.choices[0].text.strip()  
        # convert back to string
        to_string = json.dumps(generated_json)
        # appending in table
        db.execute("INSERT INTO analysis(user_id, analysis) VALUES(?, ?)", user_id, to_string) 
    except Exception as e:
        # returning
        print(f"Error extracting text from analysis: {e}")
        return None

# THis is the function that will handle creating kind of like a short summary for all the entries