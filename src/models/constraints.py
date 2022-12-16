from sqlalchemy import CheckConstraint

def positive(name: str):
    return CheckConstraint(f"{name} > 0")

def nonnegative(name: str):
    return CheckConstraint(f"{name} >= 0")

def between(name: str, min_: int, max_: int):
    return CheckConstraint(f"{name} BETWEEN {min_} AND {max_}")