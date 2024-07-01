from pydantic import BaseModel, StrictStr, EmailStr, SecretStr, Field, NonNegativeInt, Base64UrlBytes
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: Optional[int] = Field(None, alias="ID")
    username: StrictStr = Field(..., alias="UserName")
    email: EmailStr = Field(..., alias="Email")
    password: StrictStr = Field(..., alias="Password")
    usersince: Optional[datetime] = Field(None, alias="UserSince")


class AuthUser(BaseModel):
    email: EmailStr = Field(..., alias="Email")
    password: StrictStr = Field(..., alias="Password")


class Twitt(BaseModel):
    id: Optional[int] = Field(None, alias="ID")
    userid: int = Field(..., alias="UserID")
    text: Optional[StrictStr] = Field(None, alias="Text")
    picture: Optional[Base64UrlBytes] = Field(None, alias="Picture")
    createdat: Optional[datetime] = Field(None, alias="CreatedAt")
