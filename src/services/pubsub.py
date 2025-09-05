from sanic import Sanic, Request, response
from sanic.log import logger
import asyncio
import json
from uuid import UUID
from collections import defaultdict
from typing import Set, Dict, Protocol
from dataclasses import dataclass, field
from datetime import datetime
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

# In-memory pub/sub registry (replace with Redis in production)
@dataclass
class ClientSubscription:
    stream: response.HTTPResponse
    trip_ids: Set[str]

class PubSub:
    def __init__(self):
        self.subscribers: Dict[str, Set[ClientSubscription]] = defaultdict(set)

    def subscribe(self, client: ClientSubscription, trip_ids: Set[str]):
        for trip_id in trip_ids:
            self.subscribers[trip_id].add(client)
        logger.info(f"Client subscribed to trip_ids: {trip_ids}")

    def unsubscribe(self, client: ClientSubscription):
        for subscribers in self.subscribers.values():
            subscribers.discard(client)
        logger.info("Client unsubscribed")

    async def publish(self, trip_id: str, data: dict):
        for client in self.subscribers.get(trip_id, set()).copy():
            try:
                message = f"id: {data.get('message_id', 0)}\nevent: trip_update\ndata: {json.dumps(data)}\n\n"
                await client.stream.send(message)
            except Exception as e:
                logger.error(f"Error sending to client for trip_id {trip_id}: {e}")
                self.unsubscribe(client)



class Subscriber[Message](Protocol):
    def __call__(self, message: Message):
        ...

class SSESubscriber:
    def __init__(self, stream: response.HTTPResponse, accountid: UUID=None):
        self.account_id: UUID = accountid
        self.stream = stream

    async def __call__(self, message: str):
        await self.stream.send(message)


class EmailSubscriber:
    def __init__(self, email: EmailStr):
        self.email = email

    async def __call__(self, message: str):
        print(f"Sending message to {self.email}")


class SMSSubscriber:
    def __init__(self, phone_number: PhoneNumber):
        self.phone_number = phone_number

    async def __call__(self, message: str):
        print(f"Sending SMS to {self.phone_number}")

@dataclass(slots=True, repr=False, kw_only=True)
class Channel[Message]:
    subscribers: set[Subscriber[Message]] = field(default_factory=set)

    def subscribe(self, subscriber: Subscriber[Message]) -> None:
        self.subscribers.add(subscriber)

    def unsubscribe(self, subscriber: Subscriber[Message]) -> None:
        self.subscribers.remove(subscriber)

    def publish(self, message: str) -> None:
        for subscriber in self.subscribers:
            subscriber(message)

@dataclass(slots=True)
class Publisher[Message]:
    channels: dict[str, Channel[Message]] = field(default_factory=lambda: defaultdict(Channel))

    def publish(self, channel_name: str, message: str) -> None:
        self.channels[channel_name].publish(message)

    def publish_all(self, message: str) -> None:
        for channel in self.channels.values():
            channel.publish(message)

    def subscribe(self, channel_name: str, subscriber: Subscriber[Message]) -> None:
        self.channels[channel_name].subscribe(subscriber)

    def subscribe_all(self, subscriber: Subscriber) -> None:
        for channel in self.channels.values():
            channel.subscribe(subscriber)

    def unsubscribe(self, channel_name: str, subscriber: Subscriber) -> None:
        self.channels[channel_name].unsubscribe(subscriber)

    def unsubscribe_all(self, subscriber: Subscriber) -> None:
        for channel in self.channels.values():
            channel.unsubscribe(subscriber)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.channels})"

