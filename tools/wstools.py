import re

async def clear_p(input_string):
    # Define a regular expression pattern to match punctuation
    punctuation_pattern = r"[^\w\s]"

    # Use re.sub to replace punctuation with an empty string
    cleaned_string = re.sub(punctuation_pattern, "", input_string)

    return cleaned_string
