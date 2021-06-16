import datetime


class ApiObject:
    class Values:
        pass

    class BodyVariables:
        pass

    def _build_body(self) -> dict:
        primitive_types = (float, int, str, bool)
        body = {}
        for attribute, value in self.BodyVariables.__dict__.items():
            if not value:
                continue
            if type(value) in primitive_types:
                body[attribute] = value
                continue
            if type(value) == datetime.datetime:
                body[attribute] = value.timestamp()
                continue
        return body

    def _update_values(self, data: dict):
        for key, value in data.items():
            if type(value) == dict:
                if key in self.Values.__dict__:
                    setattr(self.Values, key, value)
            if key in self.Values.__dict__:
                if key in self.Values.__annotations__:
                    attr_type = self.Values.__annotations__.get(key)
                    new_value = attr_type(value)
                    setattr(self.Values, key, new_value)

