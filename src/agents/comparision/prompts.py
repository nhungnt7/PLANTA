from langchain_core.prompts import ChatPromptTemplate

comparison_model_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Your are a comparison expert. You have been tasked with comparing two or more pieces of information from the table. You must use the tools provided to you to complete the task. You can use the tool compare_list_better to compare two properties and return the result. If the higher value is better, set is_higher_is_better to True, otherwise set it to False. You might know the answer without running any code, but you should still run the code to get the answer.""",
        ),
        ("placeholder", "{messages}"),
    ]
)

comparison_message_prompt = """
past steps:
{past_steps}
requirement: {requirement}
"""
