from typing import List
from configs.config import settings

def process_table_header(columns: List[str]) -> List[str]:
    """Processes and validates table columns, ensuring they are unique and valid.
    Args:
        columns (list): List of column names.
    Returns:
        list: Processed list of unique column names.
    """
    processed_columns = []
    seen_columns = set()
    
    for i, col in enumerate(columns):
        # Remove invalid characters and replace spaces with underscores
        clean_col = ''.join(e if e.isalnum() or e == '_' else '_' for e in col).strip()
        
        # If column name is empty after cleaning, replace with "column_<index>"
        if not clean_col:
            clean_col = f"column_{i+1}"
        
        # Ensure column name is unique by appending a counter if there’s a duplicate
        original_col = clean_col
        counter = 1
        while clean_col in seen_columns:
            clean_col = f"{original_col}_{counter}"
            counter += 1
        
        seen_columns.add(clean_col)
        processed_columns.append(clean_col)
    
    return processed_columns

def format_table(table):
    if 0: #settings.CONF['llm'] == 'gpt-3.5-turbo':
        return format_csv(table)
    else:
        return format_markdown(table)

def format_markdown(table):
    """ Convert a table (list of lists) to markdown format string, with the first row as header """
    markdown_str = ""
    if table:
        # Get the header from the first row
        markdown_str += '| ' + ' | '.join(map(str, table[0])) + ' |\n'
        # Add the separator line
        markdown_str += '| ' + ' | '.join(['---'] * len(table[0])) + ' |\n'
        # Loop through the remaining rows
        for row in table[1:]:
            markdown_str += '| ' + ' | '.join(map(str, row)) + ' |\n'
    return markdown_str

def format_csv(table):
    """ Convert a table (list of lists) to CSV format string, with the first row as header """
    csv_str = ""
    if table:
        # Get the header from the first row
        csv_str += ','.join(map(str, table[0])) + '\n'
        # Loop through the remaining rows
        for row in table[1:]:
            csv_str += ','.join(map(str, row)) + '\n'
    return csv_str

def add_row_order_column(array):
    """
    Adds a 'row order' column to a two-dimensional array.
    
    Parameters:
    array (list of lists): The original two-dimensional array.

    Returns:
    list of lists: The array with the 'row order' column added.
    """
    # Add header for the 'row order' column
    array[0].insert(0, 'row order')
    
    # Add row numbers for each row
    for i in range(1, len(array)):
        array[i].insert(0, i)
    
    return array

if __name__ == "__main__":
    #test format markdown
    table = [['column1', 'column2', 'column3'], [1, 2, 3], [4, 5, 6]]
    print(format_csv(table))