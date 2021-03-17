import re
from typing import List
from datetime import datetime

from pydantic import BaseModel, ValidationError, validator


# example, pydantic validate for model
class User(BaseModel):
    id: int
    name: str = "chr"
    ts: datetime = None
    numbers: List[int] = []


def py_model_01():
    data = {
        "id": 123,
        "name": "test",
        "ts": datetime.now(),
        "numbers": [1, 2, 3]
        # "numbers": [1, 2, "a"]
    }

    try:
        user = User(**data)
        print(user.json())
        print(f"id={user.id}, name={user.name}, ts={user.ts}, numbers={user.numbers}")
    except ValidationError as e:
        print("Error:", e.json())


# example, pydantic validate for model
class UserModel(BaseModel):
    name: str
    username: str
    password1: str
    password2: str

    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalpha(), 'must be alphanumeric'
        return v

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        # values: include pre validated values
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v


def py_model_02():
    try:
        user1 = UserModel(name='samuel colvin', username='scolvin',
                          password1='zxcvbn', password2='zxcvbn')
        print(user1.json())

        user2 = UserModel(name='samuel', username='scolvin',
                          password1='zxcvbn', password2='zxcvbn2')
        print(user2.json())
    except ValidationError as e:
        print("Error:", e)


# example, vailid by Config
class Password(BaseModel):
    password: str

    class Config(object):
        min_anystr_length = 6
        max_anystr_length = 20

    @validator('password')
    def password_rule(cls, password):
        def is_valid(password):
            if not re.search("[a-z]", password):
                return False
            if not re.search("[A-Z]", password):
                return False
            if not re.search("\d", password):
                return False
            return True

        if not is_valid(password):
            raise ValueError("Password is invalid")


def py_model_03():
    pws = ['abc', '123456', 'abc123', 'Aabc123']
    for pw in pws:
        print('\ncheck password:', pw)
        try:
            p = Password(password=pw)
        except ValidationError as e:
            print("Error:", e)


if __name__ == '__main__':

    py_model_01()
    print('data model demo Done.')
