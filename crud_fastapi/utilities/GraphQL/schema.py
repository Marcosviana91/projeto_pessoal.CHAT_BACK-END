'''
Schema do GraphQL
'''
import strawberry


@strawberry.type
class User():
    id: int
    # auth_id: str  # id privado
    name: str
    photo: str
    email: str = None
    contact_list: list[int]

@strawberry.type
class UserNotification():
    timeStamp: str
    sender: str
    title: str
    content: str

@strawberry.type
class UserSessionInfo():
    user_id: str
    timeStamp: str
    status: str
    status_msg: str
    chat_list: list[int]
    notifications: list[UserNotification]


@strawberry.type
class CHATS_MSG():
    timeStamp: str
    senderId: int
    message: str
