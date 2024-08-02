class WebsiteResult:
    def __init__(self, url: str, status: int | str):
        self.url = url
        self.status = status