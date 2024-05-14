from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class JBBotUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    status: Optional[str] = None
    config_env: Optional[Dict] = {}
    version: Optional[str] = None
    channels: Optional[List[str]] = None

    class Config:
        from_attributes = True


# add credentials endpoint
class JBBotConfig(BaseModel):
    bot_id: str
    credentials: Dict = {}
    config_env: Dict = {}

    class Config:
        from_attributes = True

class JBBotChannels(BaseModel):
    whatsapp: str

# add activate bot endpoint
class JBBotActivate(BaseModel):
    phone_number: str
    channels: JBBotChannels

    class Config:
        from_attributes = True


class JBBotCode(BaseModel):
    name: str
    dsl: str
    code: str
    requirements: str
    index_urls: List[str]
    version: Optional[str] = "v0.1"
    required_credentials: Optional[List[str]] = Field(default_factory=list)

    class Config:
        from_attributes = True

class JBChannelContent(BaseModel):
    name: str
    key: str
    app_id: str
    url: str
    status: str = "inactive"

    class Config:
        from_attributes = True