""" The sole purpose of this file reflection.py is to
    contain all the functionality for AI reflection using Llama 
    and AI pattern recognising using Cerebras"""
""" Cerebras is acting as a cloud server where we can run our models 
    We will be using two different AI models each for different jobs 
    and these would be called by using Cerebras API on it's platform"""

# import useful libraries
import os
from cerebras.cloud.sdk import Cerebras

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
1.  **Length:** The output MUST be only 3-4 sentences long (maximum 100 tokens).
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
3. {"Nothing" if count == 0 else "Do not use the name or any mark left by user to identify him. Don't say hi" }

**Strict Output Format:**
1. Every response MUST be as approximately as small as 2-3 lines or as long as one short paragraphs:
2. Example: Reply to a 4-5 line text from user between 4-5 lines or a short paragraph.

1.  **Acknowledgment** (Validate the current feeling/situation).
2.  **Deep Reflection** (Connect current input to a pattern or theme from the context).
3.  **Forward Inquiry** (ONE open-ended question for deeper exploration).

---
**CURRENT REFLECTION CONTEXT (Summary):**
{summary}
---
<</SYS>>

User:{entry}
[/INST]
""".strip()

    # getting the result from Cerebaras
    completion = client.completions.create(
        prompt=prompt,
        max_tokens=200,
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