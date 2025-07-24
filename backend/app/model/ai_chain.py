import os
import requests

class TutorlyAI:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        if not self.api_key:
            raise ValueError("Gemini API key not found.")
        
        self.prompt_template = (
            "### SYSTEM INSTRUCTIONS ###\n"
            "You are an expert reviewer. Your task is to read the provided document text and extract the most important key points or a concise summary.\n\n"
            "**Guidelines:**\n"
            "- Focus on clarity and brevity\n"
            "- Use bullet points if possible\n"
            "- Avoid unnecessary details\n"
            "- Highlight only the most relevant information\n"
            "- Respond in valid GitHub Flavored Markdown (GFM) format.\n"
            "- Use markdown lists, headings, and formatting where appropriate.\n\n"
            "### DOCUMENT TEXT ###\n"
            "{content}\n\n"
            "### OUTPUT (in markdown) ###\n"
            "Provide your key points or summary below as markdown:\n"
        )

    def get_key_points(self, text: str) -> str:
        """
        Sends the input text to Gemini API and returns the key points as a string.
        """
        prompt = self.prompt_template.format(content=text)
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        data = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
        response = requests.post(self.api_url, headers=headers, params=params, json=data)
        if response.status_code == 200:
            result = response.json()
            try:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                return "Could not parse Gemini response."
        else:
            return f"Gemini API error: {response.status_code} - {response.text}"
