def check_prime(number: int) -> bool:
    """
    Check if a number is prime.
    Args:
		number (int): The number to check.
	Returns:
		dict: A dictionary containing the result of the check.
    """
    if number < 2:
        return {
            "result": False,
        }
    for i in range(2, int(number**0.5) + 1, 1):
        if number % i == 0:
            return {
                "result": False,
            }
    return {
        "result": True,
    }
