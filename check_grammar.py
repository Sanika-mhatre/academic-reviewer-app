import requests

def check_grammar(text):
    try:
        response = requests.post(
            "https://api.languagetool.org/v2/check",
            data={
                "text": text,
                "language": "en-US"
            },
            timeout=10
        )
        matches = response.json().get("matches", [])
        
        errors = []
        for match in matches:
            message = match.get("message", "Unknown error")
            replacements = [r['value'] for r in match.get("replacements", [])]
            errors.append({
                "error": message,
                "suggestions": replacements if replacements else ["No suggestion available"]
            })
        return errors

    except Exception as e:
        return [{"error": "Grammar check failed", "suggestions": [str(e)]}]
