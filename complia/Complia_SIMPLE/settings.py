import json
import os

settings_filepath = os.path.dirname(__file__) + "/" + "settings.json"

# Load settings
def load(filepath=settings_filepath):
    # Simple deserialise
    with open(filepath, 'r') as f:
        return json.load(f)

# Save settings
def save(settings, filepath=settings_filepath):
    # JSON Dump
    with open(filepath, 'w') as f:
        f.write(json.dumps(settings, indent=4))