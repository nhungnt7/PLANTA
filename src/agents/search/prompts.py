from langchain_core.prompts import ChatPromptTemplate

search_model_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
"""
You are a Text to SQL expert. You have been tasked with generate an SQL query to extract and conditional count specific information (rows) from the table. You must use the tools provided to you to complete the task. You can use the tool execute_sql to execute an SQL query generated based on the question and given table and return the result. 
Question related to order, please use "row order" to find the accurate information.
Please follow the following requirements:
- prioritize search relevant rows and columns 
- Always return the row_order for clarity.
- Use intermediate tables solely to gather additional information about the data; then, refine the final SQL statement to produce the final results.
- Pay attention to conditions that require unique results (e.g., "What is the total number of a property covered in the table?").
- For question related to 'consecutive',  interpret it as the number of pairs or tupple of consecutive rows that satisfy the condition.
- The notation "1821/22" should be understood as both 1821 and 1822.
""",
        ),
        ("placeholder", "{messages}"),
    ]
)


search_message_prompt = """
Given the table below:
Table:
{table}
Table_id (table name - please use this as database name when generate sql query): {table_id}
Please generate an SQL query then execute it to get the answer for a requirement.
Requirement: {requirement}
"""