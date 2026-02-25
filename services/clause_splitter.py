import re

def split_into_clauses(text: str):
    clauses = re.split(r'\n\d+\.\s', text)
    clauses = [c.strip() for c in clauses if len(c.strip()) > 100]
    return clauses