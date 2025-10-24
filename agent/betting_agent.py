from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from agent.prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS_BET
# Our Betting Agent

class BettingAgent:
    def __init__(self, tools, model_name):
        self.tools = tools
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0
        )
        self.prompt = PromptTemplate(
            input_variables=["input", "agent_scratchpad, tools"],
            template = REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS_BET
        ).partial(
            tools = [getattr(t, "name", t.__class__.__name__) for t in tools],
            tool_names = [getattr(t, "name", t.__class__.__name__) for t in tools]
        )
        self.agent = create_react_agent(
            tools=tools,
            llm=self.llm,
            prompt=self.prompt
        )
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True, handle_parsing_errors=True)
    
    def run(self, query):
        self.executor.invoke({"input": query})

