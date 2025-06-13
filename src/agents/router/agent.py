import os
from langchain_openai import ChatOpenAI

from src.graph.state import GraphState
from src.agents.router.schemas import QuestionType
from src.agents.router.prompts import router_prompt_template
from configs.config import settings


class RouterAgent:
    def __init__(self, llm, **kwargs):
        if "gpt" in llm:
            api_key = os.getenv("OPENAI_API_KEY")
        else:
            api_key = os.getenv("OPENSOURE_API_KEY")
        self.model = ChatOpenAI(
            model=settings.CONF["model"][llm],
            base_url=settings.CONF["base_url"][llm],
            api_key=api_key,
            temperature=settings.CONF["params"]["default_temperature"],
        )
        self.router = router_prompt_template | self.model.with_structured_output(
            QuestionType
        )

    async def agent_async(self, state: GraphState):
        past_steps = state["past_steps"]
        plan = state["plan"]
        try:
            for step in plan:
                if step not in past_steps:
                    requirement = step
                    break
        except:
            requirement = "please answer the question based on the table"

        agent_execution = await self.router.ainvoke(
            {"messages": [("user", requirement)]}
        )
        agent_execution = agent_execution.question_type
        return {"next_requirement_type": agent_execution}


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    agent = RouterAgent("gpt-4o-mini")
    state = {
        "question": "What is the total number of people who have a dog?",
        "table_id": "table1",
        "table": [
            ["Name", "Age", "Has a dog"],
            ["Alice", "25", "Yes"],
            ["Bob", "30", "No"],
        ],
        "plan": ["What is the total number of people who have a dog?"],
        "past_steps": [],
        "next_requirement_type": 0,
        "response": "",
    }
    print(agent.agent(state))

    import asyncio

    response = asyncio.run(agent.agent_async(state))
    print(response)
