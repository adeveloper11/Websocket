from time import sleep
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
import asyncio
from asgiref.sync import async_to_sync


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):  # client initialt ask to open connection
        # print('websocket connected...', event)
        # print("Channel Layer...", self.channel_layer)
        # print("Channel Name...", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print("group name...", self.group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        self.send({
            'type': 'websocket.accept'  # accept the connection
        })

    def websocket_receive(self, event):  # when we get some messate from the client
        print("Message received from client", event['text'])
        print("Type of message received from client", type(event['text']))
        async_to_sync (self.channel_layer.group_send)(
            self.group_name ,
            {
            'type': 'chat.message',
            "message":event['text']
            }
        )

    def chat_message(self, event):
        print("Event...", event)
        print('Actual Data...', event['message'])
        self.send({
            'type': 'websocket.send',
            'text': event['message']   #mesage will sented back to frontend event to show
        })
        # for i in range(10):
        #     self.send({  # application send message to client
        #         'type': 'websocket.send',
        #         'text': str(i)
        #     })
        #     sleep(1)

    def websocket_disconnect(self, event):
        print("websocket Disconnected...", event)
        print("Channel Layer...", self.channel_layer)
        print("Channel Name...", self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    # client initialt ask to open connection
    async def websocket_connect(self, event):
        print('websocket connected...', event)
        await self.send({
            'type': 'websocket.accept'  # accept the connection
        })

    # when we get some messate from the client
    async def websocket_receive(self, event):
        print("message received from client", event)
        print(event['text'])
        for i in range(50):
            await self.send({  # application send message to client
                'type': 'websocket.send',
                'text': str(i)
            })
            await asyncio.sleep(1)

    async def websocket_disconnect(self, event):
        print("websocket Disconnected...", event)
        raise StopConsumer()
