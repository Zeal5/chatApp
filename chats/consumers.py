import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .tasks import save_message_task, save_file_task


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"].get("room_name")
        if not self.room_name or self.room_name == "None":
            await self.close()
            return

        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # check if it is a text
        msg_type = data.get("type", "text")
        sender_username = data["sender"]

        if msg_type == "text":
            message = data["message"]
            # Save message to DB using celery
            save_message_task.delay(sender_username, self.room_name, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender_username,
                },
            )

        # check if it is a file
        if msg_type == "file":
            # @DEV add if filzeSize > 20MB raise event
            filename = data.get("name")
            file_data_base64 = data.get("data")
            temp_id = data.get("temp_id")
            file_size = data.get("size")
            mime_type = data.get("mime_type")

            save_file_task.delay(
                sender_username,
                self.room_name,
                file_data_base64,
                filename,
                self.room_group_name,
                temp_id,
                mime_type,
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "file_preview",
                    "message": "File received",
                    "sender": sender_username,
                    "filename": filename,
                    "temp_id": temp_id,
                    "name": filename,
                    "size": file_size,
                    "mime_type": mime_type,
                },
            )

    async def file_preview(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "file_preview",
                    "sender": event["sender"],
                    "filename": event["filename"],
                    "tempId": event["temp_id"],
                    "size": event["size"],
                    "name": event["name"],
                    "mime_type": event["mime_type"],
                }
            )
        )

    # Receive file from a room group
    async def file_uploaded(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "file_uploaded",
                    "file_url": event["file_url"],
                    "sender": event["sender"],
                    "filename": event["filename"],
                    "tempId": event["temp_id"],
                    "mime_type": event["mime_type"],
                    "name": event["filename"],
                }
            )
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sender": sender,
                }
            )
        )
