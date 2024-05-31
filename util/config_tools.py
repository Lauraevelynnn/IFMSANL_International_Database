import configparser
import re

def interpolate_vars(value, variables):
    # Find all variable names in the value
    var_names = re.findall(r'\$\{(\w+)\}', value)
    
    # Replace each variable with its value from the variables dictionary
    for var_name in var_names:
        if var_name in variables:
            value = value.replace(f'${{{var_name}}}', str(variables[var_name]))
    
    # Handle special characters interpretation
    value = value.encode().decode('unicode_escape')
    
    return value

def read_config(filename, variables):
    config = configparser.ConfigParser()
    config.read(filename)
    
    # Interpolate variables in each value
    for section in config.sections():
        for option in config.options(section):
            config.set(section, option, interpolate_vars(config.get(section, option), variables))
    
    return config