from datetime import date

from pydantic import BaseModel, UUID4


class FileBase(BaseModel):
    filename: str
    content_type: str


class FileCreate(FileBase):
    pass


class FileUpdate(FileBase):
    pass


class FileInDBBase(FileBase):
    id: UUID4
    upload: date

    class Config:
        orm_mode = True


class File(FileInDBBase):
    pass


class FileInDB(FileInDBBase):
    pass
