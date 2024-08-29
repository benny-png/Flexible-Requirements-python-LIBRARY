from packaging import version

def is_valid_version(v):
    """Check if a version string is valid."""
    try:
        version.parse(v)
        return True
    except version.InvalidVersion:
        print(f"Invalid version: {v}")  # Debug print
        return False

