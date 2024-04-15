from datetime import datetime
from tinydb import TinyDB, Query
from .db_models import User, UserSessionInfo, CHATS_MSG, CHATS, MSG_TABLE


# lista de tudo que precisa ser importado com o "from este_modulo import * ""
__all__ = []


class DB_Manager:
    engine = None
    PAGINATION = 10

    def __init__(self) -> None:
        self.engine = TinyDB('./crud_fastapi/data/db.json')

    def createNewUser(self, auth_id: str, name: str, photo: str | None, email: str, **kwargs) -> int:
        user = User(auth_id=auth_id, name=name, photo=photo,
                    email=email, contact_list=[])
        timeStamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        user_id = self.engine.table('users').insert(user.model_dump())
        user.id = user_id
        self.engine.table("users").update(user, doc_ids=[user_id])
        self.engine.table('messages').insert({
            "user_id": str(user_id),
            "timeStamp": timeStamp,
            "chats": []

        })
        self.engine.table("session_info").insert({
            "user_id": str(user_id),
            "timeStamp": timeStamp,
            "status": "on",
            "status_msg": "Acabei de entrar...",
            "chat_list": [],
            "notifications": [],
        })
        return user

    # Obtenções

    def getContextUser(self, user_id: int) -> User:
        user = self.engine.table('users').get(doc_id=user_id)
        # user["auth_id"]=''
        return User(**user)

    def getUser(self, user_id: int) -> User:
        user = self.engine.table('users').get(doc_id=user_id)
        # user["auth_id"]=''
        return User(**user)

    def getUsersByIds(self, user_ids: list[int]) -> list[User]:
        tempArray: list[User] = []
        for id in user_ids:
            user = self.engine.table('users').get(doc_id=id)
            user["auth_id"] = ''
            user["contact_list"] = []
            tempArray.append(User(**user))
        return tempArray

    def getUserSessionInfoById(self, user_id: int) -> UserSessionInfo:
        userSessionInfo = self.engine.table('session_info').get(doc_id=user_id)
        return UserSessionInfo(**userSessionInfo)

    def getUserIdByAuthID(self, auth_id: str) -> int:
        UserQuery = Query()
        ids = []
        user_id = self.engine.table('users').search(
            UserQuery.auth_id == auth_id)
        # user_id = self.engine.table('users').search(
        # UserQuery.auth_id.search(f'{auth_id}+'))
        for id in user_id:
            ids.append(id.doc_id)
        return ids

    def getUserDataByName(self, user_name: str) -> list[User]:
        import re
        UserQuery = Query()
        users = []
        if user_name == '':
            user_name = '.'
        # user_id = self.engine.table('users').search(UserQuery.auth_id == auth_id)
        try:
            resp = self.engine.table('users').search(
                UserQuery.name.search(f'{user_name}+', re.IGNORECASE))
            for user in resp:
                user['id'] = str(user.doc_id)
                users.append(User(**user))
        except Exception as e:
            print(__name__, 'Deu erro no módulo', __name__)
            print('')
            print(e)
        return users

    def getAllUser(self) -> list[User]:
        resp = self.engine.table('users').all()
        users = []
        for user in resp:
            users.append(User(**user))
        return users

    def getMessageHistory(self, user_id: str, receiverId: str, last_message: str = '') -> any:
        pre_response = []
        final_response = []
        last_message_index = None
        resp = MSG_TABLE(**self.engine.table('messages').get(doc_id=user_id))

        # get only receiverId chat
        for chat in resp.chats:
            if chat.receiverId == receiverId:
                pre_response = chat.messages
                break

        # get last_message index
        for msg in pre_response:
            if msg.timeStamp == last_message:
                last_message_index = pre_response.index(msg)

        # set final_response
        if last_message_index:
            final_response = pre_response[last_message_index -
                                          self.PAGINATION:last_message_index]
            if last_message_index < self.PAGINATION:
                final_response = pre_response[:last_message_index]
        else:
            final_response = pre_response[-self.PAGINATION:]
        return final_response

    # Inserções

    def addContact(self, user_id: int, contact_id: int) -> User:
        errorMessage = User(name='', id="0", auth_id="",
                            email="", photo="", contact_list=[])
        if user_id == contact_id:
            print(__name__, 'Não é possível adicionar a si mesmo como contato.')
            errorMessage.name = "Não é possível adicionar a si mesmo como contato."
            return errorMessage

        if (self.engine.table('users').get(doc_id=contact_id) == None):
            print(__name__, 'Contato inexistente.')
            errorMessage.name = "Contato inexistente."
            return errorMessage

        user_data = self.engine.table(
            'users').get(doc_id=user_id)
        if not user_data:
            print(
                f'Não foi possível encontrar a lista de contatos do usuário {user_id}')
            errorMessage.name = f'Não foi possível encontrar a lista de contatos do usuário {
                user_id}'
            return errorMessage

        if contact_id in user_data['contact_list']:
            print(__name__, 'Este contato já está em sua lista')
            errorMessage.name = 'Este contato já está em sua lista'
            return errorMessage

        user_data['contact_list'].append(contact_id)
        self.engine.table('users').update(user_data, doc_ids=[user_id])
        return User(**user_data)

    def removeContact(self, user_id: int, contact_id: int) -> User:
        errorMessage = User(name='', id="0", auth_id="",
                            email="", photo="", contact_list=[])
        if user_id == contact_id:
            print('Não é possível remover a si mesmo dos contatos.')
            errorMessage.name = 'Não é possível remover a si mesmo dos contatos.'
            return errorMessage

        user_data = self.engine.table(
            'users').get(doc_id=user_id)
        if not user_data:
            print(__name__,
                  f'Não foi possível encontrar os dados do usuário {user_id}')
            errorMessage.name = f'Não foi possível encontrar os dados do usuário {
                user_id}'
            return errorMessage

        if contact_id not in user_data['contact_list']:
            print(__name__,
                  f'Contato {contact_id} não está na lista do usuário {user_id}')
            errorMessage.name = f'Contato {
                contact_id} não está na lista do usuário {user_id}'
            return errorMessage

        user_data['contact_list'].remove(contact_id)
        self.engine.table('users').update(user_data, doc_ids=[user_id])
        return User(**user_data)

    def newMessage(self, user_id: int, message: str, receiverId: int) -> CHATS_MSG:
        __sended = False
        # Inserir mensagem no chat do sender
        timeStamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        new_message = CHATS_MSG(
            senderId=user_id, timeStamp=timeStamp, message=message)
        messages = MSG_TABLE(
            **self.engine.table('messages').get(doc_id=user_id))

        for chat in messages.chats:
            if chat.receiverId == receiverId:
                chat.messages.append(new_message)
                __sended = True
        if not __sended:
            messages.chats.append(
                CHATS(receiverId=receiverId, messages=[new_message]))

        self.engine.table('messages').update(
            messages.model_dump(), doc_ids=[int(user_id)]
        )
        # Inserir mensagem no chat do receiver
        if (user_id != receiverId):
            __sended = False
            messages = MSG_TABLE(
                **self.engine.table('messages').get(doc_id=receiverId))

            for chat in messages.chats:
                if chat.receiverId == user_id:
                    chat.messages.append(new_message)
                    __sended = True
            if not __sended:
                messages.chats.append(
                    CHATS(receiverId=user_id, messages=[new_message]))

            self.engine.table('messages').update(
                messages.model_dump(), doc_ids=[int(receiverId)]
            )

        return new_message

# ATÉ AQUI TUDO OK ^^
