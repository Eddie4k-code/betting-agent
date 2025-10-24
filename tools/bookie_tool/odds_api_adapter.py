import requests
from tools.bookie_tool.bookie_api_config import BookieAPIConfig
from tools.bookie_tool.bookie_api_interface import BookieAPIInterface
from langchain_core.tools import StructuredTool
import inspect

class TheOddsAPIAdapter(BookieAPIInterface):
    def __init__(self, bookie_api_config, http_client):
        super().__init__()
        self.bookie_api_config = bookie_api_config
        self.http_client = http_client

    def _get(self, endpoint):
        url = f"{self.bookie_api_config.base_url}/{endpoint}"
        try:
            return self.http_client.get(endpoint)
        except Exception as e:
            raise RuntimeError(f"ODDS API Request Failed for {url}: {e}")


    def get_sports(self):
        """
        Returns a list of in-season sport objects. The sport key can be used as the sport parameter in other endpoints.
        """
        return self._get(self.bookie_api_config.base_url)


    def get_odds(self, sport: str, regions="us", markets="h2h"):
        """
        params:
            sport: The sport key obtained from calling the /sports endpoint. upcoming is always valid, returning any live games as well as the next 8 upcoming games across all sports
            regions: Determines the bookmakers to be returned. For example, us, us2 (United States), uk (United Kingdom), au (Australia) and eu (Europe). Multiple regions can be specified if comma delimited.
            markets:  Optional - Determines which odds market is returned. Defaults to h2h (head to head / moneyline). Valid markets are h2h (moneyline), spreads (points handicaps), totals (over/under) and outrights (futures). Multiple markets can be specified if comma delimited. spreads and totals markets are mainly available for US sports and bookmakers at this time.

        Returns a list of upcoming and live games with recent odds for a given sport, region and market
        """

        return self._get("/v4/sports/{sport}/odds/?regions={regions}&markets={markets}")

    def get_scores(self, sport: str):
        """
        params:
            sport: The sport key obtained from calling the /sports endpoint.

        Returns a list of upcoming, live and recently completed games for a given sport. Live and recently completed games contain scores. Games from up to 3 days ago can be returned using the daysFrom parameter. Live scores update approximately every 30 seconds.
        """
        return self._get("/v4/sports/{sport}/scores")

    

    def get_events(self, sport: str):
        """
        params:
            sport: The sport key obtained from calling the /sports endpoint.

        Returns a list of in-play and pre-match events for a specified sport or league. The response includes event id, home and away teams, and the commence time for each event. Odds are not included in the response.        
        """
        return self._get("/v4/sports/{sport}/events")
    

    def get_event_odds(self, sport: str, eventId: str, regions="us", markets="h2h"):
        """
        params:
            eventId: The id of an upcoming or live game. Event ids can be found in the "id" field in the response of the events endpoint.
            sport: The sport key obtained from calling the /sports endpoint. upcoming is always valid, returning any live games as well as the next 8 upcoming games across all sports
            regions: Determines the bookmakers to be returned. For example, us, us2 (United States), uk (United Kingdom), au (Australia) and eu (Europe). Multiple regions can be specified if comma delimited.

        Returns odds for a single event. Accepts any available betting markets using the markets parameter. Coverage of non-featured markets is currently limited to selected bookmakers and sports, and expanding over time.

        When to use this endpoint: Use this endpoint to access odds for any supported market. Since the volume of data returned can be large, these requests will only query one event at a time. If you are only interested in the most popular betting markets, including head-to-head (moneyline), point spreads (handicap), over/under (totals), the main /odds endpoint is simpler to integrate and more cost-effective.
        """
        return self._get("/v4/sports/{sport}/events/{eventId}/odds?apiKey={apiKey}&regions={regions}&markets={markets}")

    def get_participants(self, sport:str):
        """

        params:
            sport: The sport key obtained from calling the /sports endpoint. upcoming is always valid, returning any live games as well as the next 8 upcoming games across all sports

        Returns list of participants for a given sport. Depending on the sport, a participant can be either a team or an individual. For example for NBA, a list of teams is returned. For tennis, a list of players is returned.

        This endpoint does not return players on a team.

        The returned list should be treated as a whitelist and may include participants that are not currently active.
        """

        return self._get("/v4/sports/{sport}/participants")
    
    def as_tools(self):
        tools = []
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.startswith("get_"):  # only expose intended endpoints
                def make_wrapper(fn):
                    def wrapper(*args, **kwargs):
                        return fn(*args, **kwargs)
                    wrapper.__doc__ = fn.__doc__ or f"Tool for {fn.__name__}"
                    return wrapper

                tools.append(
                    StructuredTool.from_function(
                        make_wrapper(method),
                        name=name,
                        description=method.__doc__ or f"Tool for {name}"
                    )
                )
        return tools

            
