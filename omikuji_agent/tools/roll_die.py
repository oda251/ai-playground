import random

def roll_die():
    """
    Roll an 6-sided die and return the result.
    Args:
        None
    Returns:
        dict: {"result": int, "status": str}
    """
    return {
        "result": random.randint(1, 6),
        "status": "success",
    }
