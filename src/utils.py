import yaml
import re

def load_yaml(file_path):
    """Load the YAML content from a file."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def get_value(key):
    """Retrieve a value from the loaded YAML data based on the provided key."""
    data = load_yaml('../config/config.yaml')
    return data.get(key)

def validate_regex(regex, value):
    # Validate a given regex and output if valid 
    if re.match(regex, value):
        return True
    else : 
        return False
    
def validate_subjectid(id):
    try:
        if int(id) > 0 and int(id) <=999 :
            return True
        return False
    except:
        return False