class BookieAPIConfig:
    """
    Class for holding config related to the Bookie API that is utilized
    """
    def __init__(self, API_KEY):
        self.base_url =  "https://api.the-odds-api.com/v4/?apiKey={API_KEY}"