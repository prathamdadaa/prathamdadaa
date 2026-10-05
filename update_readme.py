import os
import google.generativeai as genai

# Gemini API Configure
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("API Key missing! Please set GEMINI_API_KEY in Repository Secrets.")
    exit(1)

genai.configure(api_key=api_key)

# Read current README
readme_path = "README.md"
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        current_readme = f.read()
else:
    current_readme = "# Pratham Dada\nBCA Student & Developer"

prompt = f"""
You are an expert GitHub Profile README Architect. 
Analyze the following GitHub Profile README content and refactor it to make it exceptionally professional, modern, and high-impact.

Instructions:
1. Keep all personal identity intact (Name: Pratham Dada, Role: Developer / BCA Student).
2. Improve formatting using clean Markdown, shields.io badges, neat headers, and proper section organization (About Me, Tech Stack, Projects, GitHub Stats).
3. Do NOT remove useful existing links or stats widgets if present.
4. Output ONLY the raw Markdown content. Do not wrap in ```markdown code blocks.

Current README content:
{current_readme}
"""

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    updated_content = response.text.strip()

    # Clean markdown backticks if AI adds them
    if updated_content.startswith("```markdown"):
        updated_content = updated_content[11:]
    if updated_content.startswith("```"):
        updated_content = updated_content[3:]
    if updated_content.endswith("```"):
        updated_content = updated_content[:-3]

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content.strip())

    print("README.md successfully analyzed and updated!")

except Exception as e:
    print(f"Error while updating README: {e}")
