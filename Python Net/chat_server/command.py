import json
from abc import abstractmethod, ABC
from typing import List, Dict, Type

from chat_server.client_handler import ClientHandler
from patterns import Serializable


class Command(Serializable):
    """
    when all subclasses performing serialize, need to add a 'type' to refer to own class name.
    """
    all_command: Dict[str, Type['Command']] = None

    @staticmethod
    def get_command(type_: str):
        if Command.all_command is None:
            Command.all_command = {cmd.__name__: cmd for cmd in Command.__subclasses__()}
        return Command.all_command[type_]

    @abstractmethod
    def execute(self):
        pass


class CommandInvoker(Serializable):
    commands: List[Command]
    _receiver: ClientHandler

    def __init__(self):
        self.commands = []

    def store_command(self, command: Command) -> None:
        self.commands.append(command)

    def send_all(self):
        for command in self.commands:
            command.execute()

    def serialize(self) -> str:
        data = [command.serialize() for command in self.commands]
        return json.dumps(data)

    def set_receiver(self, receiver: ClientHandler):
        self._receiver = receiver

    def unserialize(self, serialized: str):
        assert self._receiver is not None, 'Must specify the receiver before unserializing.'

        data = []
        for command in json.loads(serialized):
            json_command = json.loads(command)
            cmd_class = Command.get_command(json_command['type'])
            _command = cmd_class(self._receiver)
            _command.unserialize(command)
            data.append(_command)

        self.commands = data


class Register(Command):

    username: str
    password: str
    client_handler: ClientHandler

    def __init__(self, client_handler: ClientHandler = None):
        self.client_handler = client_handler

    def execute(self):
        self.client_handler.register(self.username, self.password)

    def serialize(self) -> str:
        data = {
            'type': self.__class__.__name__,
            'username': self.username,
            'password': self.password
        }
        return json.dumps(data)

    def unserialize(self, serialized: str):
        data = json.loads(serialized)
        self.username = data['username']
        self.password = data['password']


class Login(Command):

    username: str
    password: str
    client_handler: ClientHandler

    def __init__(self, client_handler: ClientHandler = None):
        self.client_handler = client_handler

    def execute(self):
        self.client_handler.login(self.username, self.password)

    def serialize(self) -> str:
        data = {
            'type': self.__class__.__name__,
            'username': self.username,
            'password': self.password
        }

        return json.dumps(data)

    def unserialize(self, serialized: str):
        data = json.loads(serialized)
        self.username = data['username']
        self.password = data['password']


class Logout(Command):
    client_handler: ClientHandler

    def __init__(self, client_handler: ClientHandler = None):
        self.client_handler = client_handler

    def execute(self):
        self.client_handler.logout()

    def serialize(self) -> str:
        data = {
            'type': self.__class__.__name__
        }
        return json.dumps(data)

    def unserialize(self, serialized: str):
        pass


class Create(Command):

    name: str
    client_handler: ClientHandler

    def __init__(self, client_handler: ClientHandler = None):
        self.client_handler = client_handler

    def execute(self):
        self.client_handler.create(self.name)

    def serialize(self) -> str:
        data = {
            'type': self.__class__.__name__,
            'name': self.name
        }
        return json.dumps(data)

    def unserialize(self, serialized: str):
        data = json.loads(serialized)
        self.name = data['name']


class Join(Command):

    name: str
    client_handler: ClientHandler

    def __init__(self, client_handler: ClientHandler = None):
        self.client_handler = client_handler

    def execute(self):
        self.client_handler.join(self.name)

    def serialize(self) -> str:
        data = {
            'type': self.__class__.__name__,
            'name': self.name
        }
        return json.dumps(data)

    def unserialize(self, serialized: str):
        data = json.loads(serialized)
        self.name = data['name']


class Leave(Command):

    client_handler: ClientHandler

    def __init__(self, client_handler: ClientHandler = None):
        self.client_handler = client_handler

    def execute(self):
        self.client_handler.leave()

    def serialize(self) -> str:
        data = {
            'type': self.__class__.__name__
        }
        return json.dumps(data)

    def unserialize(self, serialized: str):
        pass


class Message(Command):

    message: str
    client_handler: ClientHandler

    def __init__(self, client_handler: ClientHandler = None):
        self.client_handler = client_handler

    def execute(self):
        self.client_handler.send_message(self.message)

    def serialize(self) -> str:
        data = {
            'type': self.__class__.__name__,
            'message': self.message
        }
        return json.dumps(data)

    def unserialize(self, serialized: str):
        data = json.loads(serialized)
        self.message = data['message']


class Close(Command):
    client_handler: ClientHandler

    def __init__(self, client_handler: ClientHandler = None):
        self.client_handler = client_handler

    def execute(self):
        self.client_handler.close()

    def serialize(self) -> str:
        data = {
            'type': self.__class__.__name__
        }
        return json.dumps(data)

    def unserialize(self, serialized: str):
        pass
