import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.graph.state import GraphState
from src.agents.search.prompts import search_model_prompt, search_message_prompt
from src.agents.search.tools import execute_sql
from src.utils.table import format_table
from configs.config import settings
class SearchAgent():
    def __init__(self, llm, **kwargs):
        self.tools = [execute_sql]
        if 'gpt' in llm:
            api_key = os.getenv("OPENAI_API_KEY")
        else:
            api_key = os.getenv("OPENSOURE_API_KEY")
        self.model = ChatOpenAI(model=settings.CONF['model'][llm], base_url= settings.CONF['base_url'][llm], api_key=api_key, temperature=settings.CONF['params']['search_temperature'])
        
        self.search = create_react_agent(self.model, self.tools,state_modifier=search_model_prompt)
  
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
        tool_config = {"configurable": {"table": state["table"], "table_id": state["table_id"]}}
        response = await self.search.ainvoke(input = {"messages": [("user", search_message_prompt.format(table=format_table(state["table"]), table_id=state["table_id"], requirement=requirement))]}, config = tool_config)
       
        return {
            "past_steps": [(requirement, response["messages"][-1].content)]
        }
        
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    agent = SearchAgent("gpt-4o-mini")
    state = {
        "question": "What is the total number of people who have a dog?",
        "table_id": "table1",
        "table": [["Name", "Age", "Has a dog"], ["Alice", "25", "Yes"], ["Bob", "30", "No"], ["John", "30", "Yes"]],
        "plan": ["Count the number of people who have a dog"],
        "past_steps": [],
        "next_requirement_type": 0,
        "response": ""
    }
    print(agent.agent(state))

    import asyncio
    response = asyncio.run(agent.agent_async(state))
    print(response)