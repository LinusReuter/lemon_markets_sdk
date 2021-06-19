import datetime


class ApiObject:
    class Values:
        pass

    class ParamVariables:
        pass

    def _build_params(self) -> dict:
        primitive_types = (float, int, str, bool)
        body = {}
        for attribute, value in self.ParamVariables.__dict__.items():
            if not value:
                continue
            if attribute == "__module__":
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
            if not value:
                continue
            if type(value) in [dict, list]:
                if key in self.Values.__dict__:
                    setattr(self.Values, key, value)
            if key in self.Values.__dict__:
                if key in self.Values.__annotations__:
                    attr_type = self.Values.__annotations__.get(key)
                    new_value = attr_type(value)
                    setattr(self.Values, key, new_value)
                else:
                    setattr(self.Values, key, value)
        return self

