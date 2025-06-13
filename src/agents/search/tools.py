from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig
import sqlite3
import pandas as pd

@tool
def execute_sql(query: str, config: RunnableConfig):
    """Executes an SQL query on a table and returns the result.
    Args:
        query: SQL query to execute.
    """
    # connect to sqlite database in memory
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # load table into sqlite within the same connection
    try:
        table = config.get("configurable", {}).get("table")
        table_id = config.get("configurable", {}).get("table_id")
        load_table_to_sqlite(conn, table, table_id)  # Pass the connection
    except Exception as e:
        return str(e)
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            return "The requirement is wrong, please update your plan."
        return result
    except Exception as e:
        return str(e)
    finally:
        conn.close()

def load_table_to_sqlite(conn, table, table_id='table0'):
    table_name = table_id
    # Convert the array to a DataFrame
    df = pd.DataFrame(table[1:], columns=table[0])
    
    # Save the DataFrame to the SQLite database using the provided connection
    df.to_sql(table_name, conn, if_exists='replace', index=False)

if __name__ == "__main__":
    query = "SELECT * FROM tab1"
    config = {"configurable": {"table": [["Name", "Age", "Has a dog"], ["Alice", "25", "Yes"], ["Bob", "30", "No"]], "table_id": "tab1"}}
    print(execute_sql(query, config))
