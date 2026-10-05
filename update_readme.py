import os
import time
from google import genai

# Gemini API Client setup
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ API Key missing! Check GEMINI_API_KEY in Repository Secrets.")
    exit(1)

client = genai.Client(api_key=api_key)

readme_path = "README.md"
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        current_readme = f.read()
else:
    current_readme = "# Pratham Dada\nBCA Student & Full Stack Developer"

prompt = f"""
You are an expert GitHub Profile README Architect. 
Refactor the following GitHub Profile README to make it modern, visual, highly professional, and aesthetic.

Instructions:
1. Preserve personal identity (Name: Pratham Dada, BCA Student, Developer).
2. Add tech stack badges (HTML, CSS, JS, Python, C++, SQL, React, Node.js), GitHub Stats widgets, and dynamic layout.
3. Organize into clear sections: About Me, Tech Stack, Featured Projects, GitHub Stats, Connect With Me.
4. Output ONLY pure raw Markdown content. Do NOT wrap output inside triple backtick codeblocks.

Current README:
{current_readme}
"""

# Valid Supported Gemini Models
models_to_try = ["gemini-3.8-flash", "gemini-3.1-pro-preview"]
success = False

for model_name in models_to_try:
    print(f"🔄 Trying model: {model_name}...")
    for attempt in range(1, 4):  # 3 attempts per model
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            updated_content = response.text.strip()

            # Clean code block tags if AI still wraps them
            lines = updated_content.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            
            final_readme = "\n".join(lines).strip()

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(final_readme)

            print(f"✅ README.md file successfully rewritten using {model_name}!")
            success = True
            break

        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed for {model_name}: {e}")
            if attempt < 3:
                time.sleep(5)  # Wait 5 seconds before retrying

    if success:
        break

if not success:
    print("❌ All model attempts failed. Check logs for details.")
    exit(1)
