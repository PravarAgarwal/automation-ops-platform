from pydantic import BaseModel

class UserPydantic(BaseModel):
    id: int
    name: str
    email: str

class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

u = User(id="abc", name = 12, email = 34)
# up = UserPydantic(id="abc", name = 12, email = 34)


print(u)
# print(up)