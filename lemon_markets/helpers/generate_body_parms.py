class Body:

    def _build_body(self) -> dict:
        primitive_types = (float, int, str, bool)
        body = {}
        for attribute, value in self.__dict__.items():
            print(attribute, value)

