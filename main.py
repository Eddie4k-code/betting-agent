from tools.bookie_tool import odds_api_adapter
import dotenv
from tools.bookie_tool.bookie_api_config import BookieAPIConfig
import os
from agent.betting_agent import BettingAgent
from tools.bookie_tool.odds_api_adapter import *
from http_client.requests_http_client import RequestsHTTPClient




dotenv.load_dotenv()

api_config = BookieAPIConfig(os.getenv("ODDS_API_KEY"))

http_client = RequestsHTTPClient()

odds_api = TheOddsAPIAdapter(api_config, http_client)

tools = odds_api.as_tools()

agent = BettingAgent(
    tools=tools,
    model_name="gpt-4"
)

agent.run(query="Best bets for tonights LA Dodgers vs Toronto Blue Jays (MLB) game")






