class BaseField(str):
    name: str
    def __str__(self) -> str:
        return f"{self.name}: {super().__str__()}\n"

class Event(BaseField):
    name = "event"

class Data(BaseField):
    name = "data"

class ID(BaseField):
    name = "id"

class Retry(BaseField):
    name = "retry"

class Heartbeat(BaseField):
    name = ""

def message(*fields: BaseField):
    return "".join(map(str, fields)) + "\n"
