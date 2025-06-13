import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.graph.state import GraphState
from src.agents.calculation.prompts import (
    calculation_model_prompt,
    calculation_message_prompt,
)
from src.agents.calculation.tools import multiply, minus
from configs.config import settings


class CalculationAgent:
    def __init__(self, llm, **kwargs):
        # self.tools = [multiply, minus, count]
        self.tools = [multiply, minus]
        if "gpt" in llm:
            api_key = os.getenv("OPENAI_API_KEY")
        else:
            api_key = os.getenv("OPENSOURE_API_KEY")
        self.model = ChatOpenAI(
            model=settings.CONF["model"][llm],
            base_url=settings.CONF["base_url"][llm],
            api_key=api_key,
            temperature=settings.CONF['params']['default_temperature'],
        )
        self.calculation = create_react_agent(
            self.model, self.tools, state_modifier=calculation_model_prompt
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
        response = await self.calculation.ainvoke(
            {
                "messages": [
                    (
                        "user",
                        calculation_message_prompt.format(
                            past_steps=past_steps, requirement=requirement
                        ),
                    )
                ]
            }
        )

        return {"past_steps": [(requirement, response["messages"][-1].content)]}


if __name__ == "__main__":
    from dotenv import load_dotenv
    for key in list(os.environ.keys()):
        if key in os.environ:
            del os.environ[key]
    load_dotenv()

    agent = CalculationAgent("gpt-4o-mini")
    state = {
        "question": "What is the total number of people who have a dog?",
        "table_id": "table1",
        "table": [
            ["Name", "Age", "Has a dog"],
            ["Alice", "25", "Yes"],
            ["Bob", "30", "No"],
        ],
        "plan": ["calculate: 2 + 3"],
        "past_steps": [],
        "next_requirement_type": 0,
        "response": "",
    }
    # print(agent.agent(state))

    import asyncio

    response = asyncio.run(agent.agent_async(state))
    print(response)
