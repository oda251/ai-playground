def omikuji(id: int):
    """
    Retruns a omikuji result based on the given id. id is 1-based. If id is out of range, return error.
    Args:
        id (int): The id of the fortune result.
    Returns:
        dict: {"result": str, "status": str, "input": dict}
    """
    fortunes = [
        "大吉",
        "中吉",
        "小吉",
        "吉",
        "凶",
        "大凶",
    ]

    if id < 0 or id > len(fortunes):
        return {"result": "Invalid fortune id.", "status": "error", "input": {"id": id}}
    id -= 1
    return {
        "result": fortunes[id],
        "input": {"id": id},
        "status": "success",
    }
