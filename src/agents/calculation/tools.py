from langchain_core.tools import tool
from typing import List


@tool
def multiply(a, b):
    """Returns the product of two numbers"""
    return a * b


@tool
def minus(a, b):
    """Returns the difference of two numbers"""
    return a - b

@tool
def add(a, b):
    """Returns the sum of two numbers"""
    return a + b

# @tool
# def average(a: List[float]):
#     """Returns the average of the list"""
#     return sum(a) / len(a)

# @tool
# def sum(a: List[float]):
#     """Returns the sum of the list"""
#     return sum(a)


# @tool
# def count(a: List):
#     """Returns the number of elements in the list"""
#     return len(a)
