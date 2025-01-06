from pydantic import BaseModel


class UserForm(BaseModel):
    email: str
    password: str