import strawberry
from .schema import User, UserSessionInfo, CHATS_MSG

from ..DataBaseManager import DB_Manager


db = DB_Manager()


@strawberry.type
class Query:

    get_allUsers: list[User] = strawberry.field(resolver=db.getAllUser)
    '''
    query {
        allPessoas {
            name
        }
    }
    '''
    get_userById: User = strawberry.field(resolver=db.getUser)
    '''
    query {
        getUserbyid(userId: 1) {
            name
        }
    }
    '''
    @strawberry.field
    def get_userSessionInfoById(self, user_id: int, info: strawberry.Info) -> UserSessionInfo:
        reponse = db.getUserSessionInfoById(user_id=user_id)
        if (user_id != info.context['user_id']):
            reponse.chat_list = []
            reponse.notifications = []
        print(reponse)
        return reponse
    '''
    query {
        getUsersessioninfobyid(userId: 1) {
            status
            statusMsg
            userId
            chatList
            timeStamp
            notifications {
                timeStamp
                sender
                title
                content
            }
        }
    }
    '''
    @strawberry.field
    def get_ctxt_user(self, info: strawberry.Info) -> User:
        print(__name__, "\nLogged User ID:", info.context['user_id'])
        return db.getContextUser(
            user_id=info.context['user_id'],
        )
    '''
    query {
        getCtxtUser{
            id
            name
            photo
            email
            contactList
        }
    }
    '''
    get_usersByIds: list[User] = strawberry.field(resolver=db.getUsersByIds)
    '''
    query {
        getUsersbyids(userIds:[1, 2, 3]) {
            name,
            photo
        }
    }
    '''
    search_usersByName: list[User] = strawberry.field(
        resolver=db.getUserDataByName)
    '''
    query {
        searchUsersbyname(userName:"a"){
            name
        }
    }
    '''
    @strawberry.field
    def get_ctxt_messageHistory(self, receiverId: int, last_message: str, info: strawberry.Info) -> list[CHATS_MSG]:
        return db.getMessageHistory(
            user_id=info.context['user_id'],
            receiverId=receiverId,
            last_message=last_message,
        )
    '''
    query {
        getCtxtMessagehistory( receiverId:"5", lastMessage:"") {
            senderId
            timeStamp
            message
        }
    }
    '''
