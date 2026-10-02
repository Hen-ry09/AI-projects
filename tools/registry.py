from __future__ import annotations


class Tool:
    def __init__(self, fn, name: str, description: str, parameters: dict):
        self.fn = fn
        self.name = name
        self.description = description
        self.parameters = parameters

    def to_openai_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def execute(self, **kwargs):
        return self.fn(**kwargs)


_registry: dict[str, Tool] = {}


def tool(name: str, description: str, parameters: dict):
    def decorator(fn):
        _registry[name] = Tool(fn, name, description, parameters)
        return fn

    return decorator


def get_all_tools() -> dict[str, Tool]:
    return dict(_registry)
