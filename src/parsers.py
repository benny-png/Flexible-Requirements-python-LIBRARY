import re

def parse_requirement(req_string):
    """Parse a requirement string into name and version specifier."""
    print(f"Parsing requirement: {req_string}")  # Debug print
    match = re.match(r"([^=<>~!]+)(.+)?", req_string)
    if match:
        name, version_spec = match.groups()
        print(f"Parsed: name={name.strip()}, version_spec={version_spec.strip() if version_spec else None}")  # Debug print
        return name.strip(), version_spec.strip() if version_spec else None
    print(f"Failed to parse: {req_string}")  # Debug print
    return None, None