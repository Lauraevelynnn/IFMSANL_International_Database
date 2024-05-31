from dateutil import parser
from datetime import datetime
import re

def extract_deadline(email_subject):
    # Define the regular expression pattern to match [DL:00/00]
    pattern = r"\[?DL: ?(\d{1,2}/\d{1,2})\]?"

    # Use re.search to find the pattern in the input_string
    match = re.search(pattern, email_subject)

    # If match is found, return the extracted date, otherwise return None
    if match:
        exact_deadline = parse_date(match.group(1))
        return exact_deadline
    else:
        return None

def parse_date(date_str):
    # Split the input string by spaces
    words = date_str.split()

    # Iterate through the words to find the start of the date part
    start_index = 0
    for i, word in enumerate(words):
        if re.match(r"^\d+(th|st|nd|rd)$", word):
            start_index = i
            break
    # Join the words from the start of the date part
    date_str = ' '.join(words[start_index:])

    parsed_date = parser.parse(date_str, dayfirst=True)

    # Parse the date using dateutil.parser.parse
    return parsed_date.strftime('%d/%m/%Y')

def has_date_passed(date_string):
    # Convert the date string to a datetime object
    date_format = '%d/%m/%Y'
    extracted_date = datetime.strptime(date_string, date_format)

    # Get the current date
    current_date = datetime.now()

    # Compare the extracted date with the current date
    if extracted_date < current_date:
        return True
    else:
        return False