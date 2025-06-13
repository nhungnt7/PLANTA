from langgraph.graph import END

from langgraph.graph import StateGraph, START
from src.agents.planning.agent import PlanningAgent
from src.agents.replanning.agent import ReplanningAgent
from src.agents.router.agent import RouterAgent
from src.agents.search.agent import SearchAgent
from src.agents.comparision.agent import ComparisionAgent
from src.agents.calculation.agent import CalculationAgent
from src.graph.state import GraphState


class WorkFlow:
    def __init__(self, llm) -> None:
        self.workflow = StateGraph(GraphState)
        self.llm = llm
        self.build_workflow_async()

    def build_workflow_async(self):
        # add nodes
        self.workflow.add_node("planner", PlanningAgent(self.llm).agent_async)
        self.workflow.add_node("replanner", ReplanningAgent(self.llm).agent_async)
        self.workflow.add_node("router", RouterAgent(self.llm).agent_async)
        self.workflow.add_node("search", SearchAgent(self.llm).agent_async)
        self.workflow.add_node("comparision", ComparisionAgent(self.llm).agent_async)
        self.workflow.add_node("calculation", CalculationAgent(self.llm).agent_async)

        # add edges
        self.workflow.add_edge(START, "planner")
        self.workflow.add_edge("planner", "router")
        self.workflow.add_conditional_edges(
            "router",
            self.router_condition,
            ["search", "comparision", "calculation"],
        )
        self.workflow.add_edge("search", "replanner")
        self.workflow.add_edge("comparision", "replanner")
        self.workflow.add_edge("calculation", "replanner")
        self.workflow.add_conditional_edges(
            "replanner",
            # Next, we pass in the function that will determine which node is called next.
            self.should_end,
            ["router", END],
        )

    @staticmethod
    def should_end(state: GraphState):
        if "response" in state and state["response"]:
            return END
        else:
            return "router"

    @staticmethod
    def router_condition(state: GraphState):
        agent = state["next_requirement_type"]
        if agent == 1:
            return "search"
        if agent == 2:
            return "calculation"
        if agent == 3:
            return "comparision"

    def compile(self):
        return self.workflow.compile()


if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()

    async def main():
        workflow = WorkFlow("gpt-4o-mini")
        app = workflow.compile()
        input_data = {
            "question": "What is the total number of people who have a dog?",
            "table_id": "table1",
            "table": [
                ["Name", "Age", "Has a dog"],
                ["Alice", "25", "Yes"],
                ["Bob", "30", "No"],
                ["John", "30", "No"],
            ],
        }
        config = {"recursion_limit": 50}
        # async for event in app.astream(input_data, config=config):
        #     for k, v in event.items():
        #         if k != "__end__":
        #             print(v)
        response = await app.ainvoke(input_data, config)
        print(response)

    asyncio.run(main())
