import google.generativeai as genai
import os
import PIL.Image
import io
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

ANALYSIS_PROMPT = """
You are an expert data analyst. A user uploaded an image of a data visual.
Analyze it carefully and complete ALL THREE tasks in one single response.

TASK 1 — VISUAL_TYPE:
Write one sentence identifying exactly what kind of visual this is.
Example: "This is a bar chart showing monthly revenue for 2024."

TASK 2 — DATA:
Extract every data point visible in the image and return it as valid JSON.

For bar charts, line charts, scatter plots:
{"series_name": "Revenue", "labels": ["Jan","Feb","Mar"], "values": [100,200,150]}

For pie or donut charts:
{"series_name": "Market Share", "labels": ["A","B","C"], "values": [40,35,25]}

For tables:
{"headers": ["Name","Score","Grade"], "rows": [["Alice",92,"A"],["Bob",78,"B"]]}

For dashboards extract the most prominent chart visible.
If you truly cannot extract data return: {"error": "data not extractable"}

TASK 3 — ANALYSIS:
Write 5-7 sentences analyzing this visual like a smart business consultant
explaining to a CEO. Use plain simple English — no jargon, no complex words.
A 16-year-old should be able to understand every sentence.
Cover these points:
- What is the overall story this chart is telling in one simple sentence
- What is the highest point, when did it happen, and what does it mean
- What is the lowest point and what does it mean for the business
- If there is an anomaly describe it in plain english with the exact
  numbers — for example "March jumped 67% compared to February"
- One simple recommendation that anyone can act on immediately

Return using EXACTLY this format. Nothing before VISUAL_TYPE, nothing after ANALYSIS:

VISUAL_TYPE: ...
DATA: {...}
ANALYSIS: ...
"""


def analyze_visual(image_bytes: bytes) -> dict:
    image = PIL.Image.open(io.BytesIO(image_bytes)).convert("RGB")
    response = model.generate_content([ANALYSIS_PROMPT, image])
    return {"raw": response.text, "image_bytes": image_bytes}


def chat_followup(image_bytes: bytes, chat_history: list, user_message: str) -> str:
    image = PIL.Image.open(io.BytesIO(image_bytes)).convert("RGB")
    history_text = ""
    for msg in chat_history:
        role = "User" if msg["role"] == "user" else "Analyst"
        history_text += f"{role}: {msg['content']}\n"
    full_prompt = f"""You are an expert data analyst who already analyzed this image.
Here is the conversation so far:
{history_text}
Now answer this new question about the same image: {user_message}
Be specific, reference actual data points you can see in the image, keep it concise."""
    response = model.generate_content([full_prompt, image])
    return response.text
