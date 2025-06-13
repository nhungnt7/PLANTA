import os
from langchain_openai import ChatOpenAI

from src.graph.state import GraphState
from src.agents.planning.schemas import Plan
from src.agents.planning.prompts import planner_prompt_template, planner_message_prompt
from src.utils.table import format_table
from configs.config import settings


class PlanningAgent:
    
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
        self.planner = planner_prompt_template | self.model.with_structured_output(Plan)

    async def agent_async(self, state: GraphState):
        table = state["table"]
        question = state["question"]
        table_cap = state["table_cap"]
        plan = await self.planner.ainvoke(
            {
                "messages": [
                    (
                        "user",
                        planner_message_prompt.format(
                            table=format_table(table),
                            question=question,
                            table_cap=table_cap,
                        ),
                    )
                ]
            }
        )
        return {"plan": plan.steps}


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    agent = PlanningAgent("gpt-4o-mini")
    state = {
        "question": "What is the total number of people who have a dog?",
        "table_id": "table1",
        "table": [
            ["Name", "Age", "Has a dog"],
            ["Alice", "25", "Yes"],
            ["Bob", "30", "No"],
        ],
        "plan": [],
        "past_steps": [],
        "next_requirement_type": 0,
        "response": "",
    }
    print(agent.agent(state))

    import asyncio

    response = asyncio.run(agent.agent_async(state))
    print(response)
