from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    auth_id: str  # id privado
    name: str
    photo: str | None = None
    email: str = None
    contact_list: list[int] = []
    

class UserNotification(BaseModel):
    timeStamp: str
    sender: str
    title: str
    content: str


class UserSessionInfo(BaseModel):
    user_id: int | None = None
    timeStamp: str
    status: str = "off"
    status_msg: str = "Nada ainda"
    chat_list: list[int] = []
    notifications: list[UserNotification] = []
    

class CHATS_MSG(BaseModel):
    timeStamp: str
    senderId: int
    message: str


class CHATS(BaseModel):
    receiverId: int
    messages: list[CHATS_MSG]


class MSG_TABLE(BaseModel):
    user_id: int
    timeStamp: str
    chats: list[CHATS]
