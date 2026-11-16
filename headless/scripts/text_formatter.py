# headless/scripts/text_formatter.py

def wrap_team_name(name, max_chars_per_line=15):
    """
    Takes a team name string and wraps it into lines where each line 
    is capped to approximately max_chars_per_line (default 15 characters),
    breaking cleanly between words.
    """
    if not name:
        return ""
        
    words = name.split()
    if not words:
        return name

    lines = []
    current_line_words = []
    current_line_length = 0

    for word in words:
        # Check length if we were to add this word to the current line (+1 for space)
        projected_length = current_line_length + len(word) + (1 if current_line_words else 0)
        
        if projected_length <= max_chars_per_line or not current_line_words:
            current_line_words.append(word)
            current_line_length = projected_length
        else:
            # Push current line and start a new one
            lines.append(" ".join(current_line_words))
            current_line_words = [word]
            current_line_length = len(word)
            
    # Don't forget the last line
    if current_line_words:
        lines.append(" ".join(current_line_words))

    return "\n".join(lines)