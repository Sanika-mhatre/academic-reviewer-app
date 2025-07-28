# check_grammar.py

import requests

def check_grammar(text):
    if not text.strip():
        return []

    try:
        response = requests.post(
            "https://api.languagetool.org/v2/check",
            data={
                "text": text,
                "language": "en-US"
            }
        )
        matches = response.json().get("matches", [])
        grammar_errors = [
            {
                "message": match["message"],
                "suggestions": [s["value"] for s in match.get("replacements", [])],
                "context": match["context"]["text"],
                "offset": match["context"]["offset"],
                "length": match["context"]["length"]
            }
            for match in matches
        ]
        return grammar_errors

    except Exception as e:
        return [{"message": f"Grammar API error: {str(e)}", "suggestions": [], "context": "", "offset": 0, "length": 0}]
