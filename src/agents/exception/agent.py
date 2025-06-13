import os
from langchain_openai import ChatOpenAI
from src.agents.exception.schemas import Exception_Output
from src.agents.exception.prompts import exception_prompt_template, exception_message_prompt, examples
from src.utils.table import format_table
from configs.config import settings

class HandleException():
    def __init__(self, llm, **kwargs):
        if "gpt" in llm:
            api_key = os.getenv("OPENAI_API_KEY")
        else:
            api_key = os.getenv("OPENSOURE_API_KEY")
        self.model = ChatOpenAI(
            model=settings.CONF["model"][llm],
            base_url=settings.CONF["base_url"][llm],
            api_key=api_key,
            temperature=settings.CONF["params"]["high_temperature"],
        )
        self.exception = exception_prompt_template | self.model.with_structured_output(Exception_Output)
        # self.exception = exception_prompt_template | ChatOpenAI(
        #     model=settings.CONF["model"][llm], temperature=0
        # ).with_structured_output(Exception_Output)
    
    def exception_response(self, table, table_cap, question):
        answer = self.exception.invoke({"messages": [("user", exception_message_prompt.format(table=format_table(table), table_cap=table_cap, question=question, examples=examples[settings.CONF['dataset']]))]})
        try:
            return answer.answer
        except:
            return answer

if __name__ == "__main__":
    from dotenv import load_dotenv
    from configs.config import set_config
    set_config(None)
    from configs.config import settings
    from src.utils.table import format_table

    # print dataset name
    print(f"Are Testing On Dataset: {settings.CONF['dataset']}")
    load_dotenv(override=True)

    agent = HandleException("gpt-4o-mini")
    table = [["Name", "Age", "Has a dog"], ["Alice", "25", "Yes"], ["Bob", "30", "No"]]
    question = "What is the total number of people who have a dog?"

    import asyncio
    response = asyncio.run(agent.exception_response(table, question))
    print(response)