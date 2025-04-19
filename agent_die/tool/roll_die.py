import random

def roll_die():
    """
    Roll an 8-sided die and return the result.
    Args:
        None
    Returns:
        dict: A dictionary containing the result of the die roll, tool name, and tool input.
    """
    return {
        "result": random.randint(100, 200),
        "tool_name": "roll_die",
        "tool_input": {},
    }
