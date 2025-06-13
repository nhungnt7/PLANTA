from langchain_core.prompts import ChatPromptTemplate
from configs.config import settings

replanner_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"""You are the decision-making assistant to address the task of {settings.CONF['task'][settings.CONF['dataset']]}. Your goal is to answer the question based on the current context and the steps that have been executed so far. Given that the past_steps may contain inaccurate information. 
Or remove past_steps from the original plan and continue.
            """,
        ),
        ("placeholder", "{messages}"),
    ]
)

replanner_message_prompt = """
Given the task of {task}.
Table:
{table}
Table Caption: {table_cap}
Your original plan was this:
{plan}
You have currently done the follow steps with the following results at template (step, result):
{past_steps}
If the requirement is determined to be return the answer, please respond with the answer base on past steps. 
Your question is:
{question}
"""
