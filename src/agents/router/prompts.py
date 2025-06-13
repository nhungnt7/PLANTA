from langchain_core.prompts import ChatPromptTemplate

router_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Given a question, classify the requirement type for the given question and route it to the appropriate agent.
Please return the agent type based on the following:
1. return 'sql' if you need to search, conditional count the table for specific information. (example: find the number of ships wrecked in Lake Huron).
2. return 'compare' if you need to compare two or more pieces of information. (example: compare the number of ships wrecked in Lake Huron and Lake Erie).
3. return 'calculation' if you need to perform a calculation between numbers(example: sum, average, etc.).
            """,
        ),
        ("placeholder", "{messages}"),
    ]
)
