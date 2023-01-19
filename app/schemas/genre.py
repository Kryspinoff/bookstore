from pydantic import BaseModel, validator, Field


class GenreBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=32,
        regex=r"^([a-zA-Z](\s?|-?))*([a-zA-Z])+$",
        example="action"
    )

    @validator("name")
    def valid_name(cls, value: str):
        return value.lower()

    def __hash__(self):
        return hash(tuple(self))

    def __repr__(self):
        return self.name


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    pass


class GenreInDBBase(GenreBase):
    id: int

    class Config:
        orm_mode = True


class Genre(GenreInDBBase):
    pass


class GenreInDB(GenreInDBBase):
    pass
