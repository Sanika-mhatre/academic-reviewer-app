import language_tool_python

def check_grammar(text: str):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    
    errors = [match.context for match in matches]
    total_errors = len(errors)

    return total_errors, errors
