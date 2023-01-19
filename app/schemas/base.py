from pydantic import BaseModel, root_validator


# Properties to receive via API on update
class UpdateValidator(BaseModel):
    @root_validator()
    def required_at_least_one_parameter(cls, values):
        if (
            not any(values.values())
            or list(values.keys()) in list(cls.__fields__.keys())
        ):
            raise ValueError("At least one parameter is required")
        return values