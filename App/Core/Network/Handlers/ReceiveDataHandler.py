from App import Application
from App.Core.Abstract import AbstractReceiveDataHandler
from App.Core import Config
from App.Core.Network.Protocol import RCL
from App.Core.Network.Protocol.Responses import AbstractResponse


class ReceiveDataHandler(AbstractReceiveDataHandler):
    def __init__(self, rcl: RCL):
        self.__rcl = rcl

    @staticmethod
    def __get_action_name(subcommands: list) -> str:
        if not subcommands:
            return 'invoke'

        return '_'.join(subcommands)

    def handle(self, data: bytes) -> bytes:
        request = self.__rcl.parse_request(data)

        received_data = request.data()

        action = self.__get_action_name(received_data['subcommands'])

        response = Application().call([f"controller.{received_data['command']}", action], **{
            'parameters': received_data['parameters'],
            'request': request,
        })

        if type(response) is AbstractResponse:
            return self.__rcl.create_response(response)

        return self.__rcl.response_success(response)
