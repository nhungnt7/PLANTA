import random
import os
from langchain_openai import ChatOpenAI

from src.graph.state import GraphState
from src.agents.replanning.schemas import Plan, Response, Act
from src.agents.replanning.prompts import (
    replanner_prompt_template,
    replanner_message_prompt,
)
from src.utils.table import format_table
from configs.config import settings


class ReplanningAgent:
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

        self.replanner = replanner_prompt_template | self.model.with_structured_output(
            Act
        )

    async def agent_async(self, state: GraphState, k: int = 5):
        # Set a chance to decide whether to execute the replanner
        execute_replanner = random.random() < 0 / 100

        if state["plan"] is None:
            state["plan"] = [
                "Please response to user based on previous steps and given table."
            ]

        if len(state["plan"]) == 1 or execute_replanner:
            # Execute replanner
            output = await self.replanner.ainvoke(
                {
                    "messages": [
                        (
                            "user",
                            replanner_message_prompt.format(
                                table=format_table(state["table"]),
                                table_cap=state["table_cap"],
                                question=state["question"],
                                plan=state["plan"],
                                past_steps=state["past_steps"],
                                task=settings.CONF["task"][
                                    settings.CONF["dataset"]
                                ],
                            ),
                        )
                    ]
                }
            )

            if isinstance(output.action, Plan):
                return {"plan": output.action.steps}

            if isinstance(output.action, Response):
                return {"response": output.action.response}
        else:
            # Check the last three past_steps for "sorry"
            if len(state["past_steps"]) >= k:
                last_k_responses = [
                    step[1].lower() for step in state["past_steps"][-k:]
                ]
                if all("sorry" in response for response in last_k_responses):
                    return {
                        "response": "Please answer the question directly from table the plan does not work."
                    }

            # Continue plan from the step immediately after the last one in past_steps
            last_past_step = state["past_steps"][-1][0]  # Get the last step in past_steps
            try:
                last_index = state["plan"].index(
                    last_past_step
                )  # Find its index in plan
                new_plan = state["plan"][
                    last_index + 1 :
                ]  # Continue from the next step
            except ValueError:
                # If the last step from past_steps is not in the plan, use the entire plan
                new_plan = state["plan"]

            return {"plan": new_plan}


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    agent = ReplanningAgent("gpt-4o-mini")
    state = {
        "question": "What is the total number of people who have a dog?",
        "table_id": "table1",
        "table": [
            ["Name", "Age", "Has a dog"],
            ["Alice", "25", "Yes"],
            ["Bob", "30", "No"],
        ],
        "plan": [
            "Step 1: Count the number of people who have a dog",
            "Step 2: Sum the count",
        ],
        "past_steps": ["Step 1: Count the number of people who have a dog"],
        "next_requirement_type": 0,
        "response": "",
    }
    print(agent.agent(state))

    import asyncio

    response = asyncio.run(agent.agent_async(state))
    print(response)
