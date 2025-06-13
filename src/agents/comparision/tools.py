from langchain_core.tools import tool


@tool
def compare_list_properties(list, is_higher_is_better: bool) -> str:
    """Compares properties in a list and returns the result. Note that len of list <=100. if is_higher_is_better is True, the higher value is better, otherwise the lower value is better"""
    if is_higher_is_better:
        max_value = max(list)
        return f"{max_value} is better"
    else:
        min_value = min(list)
        return f"{min_value} is better"
