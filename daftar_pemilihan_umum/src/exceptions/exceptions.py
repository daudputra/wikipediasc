class ErrorParseData(Exception):
    def __init__(self, message="Failed to parse page"):
        self.message = message
        super().__init__(self.message)


class ErrorSaveJson(Exception):
    def __init__(self, message="Failed to save json file"):
        self.message = message
        super().__init__(self.message)