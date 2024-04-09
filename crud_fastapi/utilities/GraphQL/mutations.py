import strawberry
from .schema import User, CHATS_MSG

from ..DataBaseManager import DB_Manager


db = DB_Manager()

@strawberry.type
class Mutation:
    # create_pessoa: User | None = strawberry.field(resolver=db.createNewUser)
    # '''
    # mutation {
    #     createPessoa(authId:"asdsa", name:"Maria", photo:"", email:"testedamaria@mail.com"){
    #         name
    #     }
    # }
    # '''
    # add_contact: User | None = strawberry.field(resolver=db.addContact)
    @strawberry.field
    def add_contact(self, contact_id: int, info: strawberry.Info) -> User:
        return db.addContact(
            user_id=info.context['user_id'],
            contact_id=contact_id,
        )
    '''
    mutation {
        addContact(contactId:5) {
            contactList
        }
    }
    '''
    
    # remove_contact: User | None = strawberry.field(resolver=db.removeContact)
    @strawberry.field
    def remove_contact(self, contact_id: int, info: strawberry.Info) -> User:
        return db.removeContact(
            user_id=info.context['user_id'],
            contact_id=contact_id,
        )
    '''
    mutation {
        removeContact(contactId: 11) {
            id
            name
            contactList
        }
    }
    '''
    # new_message: CHATS_MSG | None = strawberry.field(resolver=db.newMessage)
    @strawberry.field
    def new_message(self, message: str, receiverId: int, info: strawberry.Info) -> CHATS_MSG:
        return db.newMessage(
            user_id=info.context["user_id"],
            message=message,
            receiverId=receiverId,
        )
    '''
    mutation {
        newMessage(receiverId:5, message:"texto de exemplo") {
            senderId
            timeStamp
            message
        }
    }
    '''
    