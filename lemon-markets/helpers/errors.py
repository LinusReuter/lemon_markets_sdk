class BaseError(Exception):
    detail = None

    def __init__(self, detail: str):
        self.detail = detail

    def to_representation(self):
        return self.detail

    def __str__(self):
        return self.to_representation()

    def __repr__(self):
        return self.to_representation()
