from pydantic import BaseModel, validator, EmailStr

user_roles = ["manager", "admin", "super admin"]

class Search(BaseModel):
    first_name: str = None
    last_name: str = None
    email: EmailStr = None

class Update(BaseModel):
    first_name: str = None
    last_name: str = None

class Retrieve(BaseModel):
    user_id: int

class Reset(BaseModel):
    old_password: str
    new_password: str

class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    privilege: str = "manager"
    @validator('privilege')
    def c_match(cls, value):
        value = value.lower().strip()
        if value not in user_roles:
            raise ValueError(f'user role must be in {user_roles}')
        return value
    @validator('password')
    def password_length(cls, value):
        if len(value)<5:
            raise ValueError('Password must be at least 5 characters long.')
        return value

class ForgotPassword(BaseModel):
    email: EmailStr