import datetime


class ApiObject:
    class RespondVariables:
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

    def _set_data(self, data: dict):
        for key, value in data.items():
            if type(value) == dict:
                self._set_data(value)
            if key in self.RespondVariables.__dict__:
                if key in self.RespondVariables.__annotations__:
                    attr_type = self.RespondVariables.__annotations__.get(key)
                    new_value = attr_type(value)
                    setattr(self.RespondVariables, key, new_value)

