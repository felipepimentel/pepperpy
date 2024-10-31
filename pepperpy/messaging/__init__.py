"""Messaging system for asynchronous communication."""
from typing import Any, Dict, Optional, Callable, List, Union
from dataclasses import dataclass, field
import json
import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from loguru import logger

@dataclass
class MessageConfig:
    """Configuration for messaging system."""
    broker_url: str
    queue_name: str
    exchange: str = ""
    routing_key: str = ""
    durable: bool = True
    auto_delete: bool = False
    prefetch_count: int = 1
    retry_count: int = 3
    retry_delay: float = 1.0
    dead_letter_exchange: Optional[str] = None

@dataclass
class Message:
    """Represents a message in the system."""
    content: Any
    message_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    headers: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0

class MessageBroker(ABC):
    """Abstract base class for message brokers."""
    
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to broker."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Close broker connection."""
        pass
    
    @abstractmethod
    async def publish(
        self,
        message: Message,
        routing_key: Optional[str] = None
    ) -> None:
        """Publish a message."""
        pass
    
    @abstractmethod
    async def subscribe(
        self,
        callback: Callable[[Message], Any],
        queue: Optional[str] = None
    ) -> None:
        """Subscribe to messages."""
        pass

class RabbitMQBroker(MessageBroker):
    """RabbitMQ implementation."""
    
    def __init__(self, config: MessageConfig):
        self.config = config
        self._connection = None
        self._channel = None
        self._consuming = False
    
    async def connect(self) -> None:
        """Connect to RabbitMQ."""
        import aio_pika
        
        try:
            self._connection = await aio_pika.connect_robust(
                self.config.broker_url
            )
            self._channel = await self._connection.channel()
            await self._channel.set_qos(
                prefetch_count=self.config.prefetch_count
            )
            
            # Declare exchange if specified
            if self.config.exchange:
                await self._channel.declare_exchange(
                    self.config.exchange,
                    aio_pika.ExchangeType.TOPIC,
                    durable=self.config.durable
                )
            
            # Declare queue
            await self._channel.declare_queue(
                self.config.queue_name,
                durable=self.config.durable,
                auto_delete=self.config.auto_delete
            )
            
            logger.info(f"Connected to RabbitMQ: {self.config.broker_url}")
            
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from RabbitMQ."""
        if self._consuming:
            await self._channel.close()
        if self._connection:
            await self._connection.close()
            self._connection = None
            self._channel = None
    
    async def publish(
        self,
        message: Message,
        routing_key: Optional[str] = None
    ) -> None:
        """Publish message to RabbitMQ."""
        import aio_pika
        
        if not self._channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        try:
            # Prepare message
            message_data = {
                "content": message.content,
                "message_id": message.message_id,
                "timestamp": message.timestamp.isoformat(),
                "headers": message.headers
            }
            
            # Create AMQP message
            amqp_message = aio_pika.Message(
                body=json.dumps(message_data).encode(),
                message_id=message.message_id,
                timestamp=message.timestamp,
                headers=message.headers,
                priority=message.priority
            )
            
            # Publish
            routing_key = routing_key or self.config.routing_key
            if self.config.exchange:
                exchange = await self._channel.get_exchange(
                    self.config.exchange
                )
                await exchange.publish(
                    amqp_message,
                    routing_key=routing_key
                )
            else:
                await self._channel.default_exchange.publish(
                    amqp_message,
                    routing_key=self.config.queue_name
                )
                
            logger.debug(f"Published message: {message.message_id}")
            
        except Exception as e:
            logger.error(f"Failed to publish message: {str(e)}")
            raise
    
    async def subscribe(
        self,
        callback: Callable[[Message], Any],
        queue: Optional[str] = None
    ) -> None:
        """Subscribe to messages from RabbitMQ."""
        if not self._channel:
            raise RuntimeError("Not connected to RabbitMQ")
            
        async def process_message(message):
            async with message.process():
                try:
                    # Parse message
                    message_data = json.loads(message.body.decode())
                    msg = Message(
                        content=message_data["content"],
                        message_id=message_data["message_id"],
                        timestamp=datetime.fromisoformat(
                            message_data["timestamp"]
                        ),
                        headers=message_data["headers"]
                    )
                    
                    # Process message
                    await callback(msg)
                    
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
                    # Requeue message if retries available
                    if message.headers.get("retry_count", 0) < self.config.retry_count:
                        await asyncio.sleep(self.config.retry_delay)
                        await message.nack(requeue=True)
                    else:
                        # Send to dead letter exchange if configured
                        if self.config.dead_letter_exchange:
                            await self._channel.default_exchange.publish(
                                message,
                                routing_key=self.config.dead_letter_exchange
                            )
                        await message.reject()
        
        # Start consuming
        queue = queue or self.config.queue_name
        queue_obj = await self._channel.declare_queue(queue)
        await queue_obj.consume(process_message)
        self._consuming = True
        
        logger.info(f"Subscribed to queue: {queue}")

class KafkaBroker(MessageBroker):
    """Kafka implementation."""
    
    def __init__(self, config: MessageConfig):
        self.config = config
        self._producer = None
        self._consumer = None
    
    async def connect(self) -> None:
        """Connect to Kafka."""
        from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
        
        try:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.config.broker_url
            )
            await self._producer.start()
            
            logger.info(f"Connected to Kafka: {self.config.broker_url}")
            
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {str(e)}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from Kafka."""
        if self._producer:
            await self._producer.stop()
            self._producer = None
        if self._consumer:
            await self._consumer.stop()
            self._consumer = None
    
    async def publish(
        self,
        message: Message,
        routing_key: Optional[str] = None
    ) -> None:
        """Publish message to Kafka."""
        if not self._producer:
            raise RuntimeError("Not connected to Kafka")
            
        try:
            # Prepare message
            message_data = {
                "content": message.content,
                "message_id": message.message_id,
                "timestamp": message.timestamp.isoformat(),
                "headers": message.headers
            }
            
            # Publish
            topic = routing_key or self.config.routing_key or self.config.queue_name
            await self._producer.send_and_wait(
                topic,
                json.dumps(message_data).encode()
            )
            
            logger.debug(f"Published message to topic {topic}: {message.message_id}")
            
        except Exception as e:
            logger.error(f"Failed to publish message: {str(e)}")
            raise
    
    async def subscribe(
        self,
        callback: Callable[[Message], Any],
        queue: Optional[str] = None
    ) -> None:
        """Subscribe to messages from Kafka."""
        from aiokafka import AIOKafkaConsumer
        
        topic = queue or self.config.queue_name
        
        try:
            self._consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=self.config.broker_url,
                group_id=self.config.queue_name
            )
            await self._consumer.start()
            
            async for msg in self._consumer:
                try:
                    # Parse message
                    message_data = json.loads(msg.value.decode())
                    message = Message(
                        content=message_data["content"],
                        message_id=message_data["message_id"],
                        timestamp=datetime.fromisoformat(
                            message_data["timestamp"]
                        ),
                        headers=message_data["headers"]
                    )
                    
                    # Process message
                    await callback(message)
                    
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
                    
            logger.info(f"Subscribed to topic: {topic}")
            
        except Exception as e:
            logger.error(f"Failed to subscribe to Kafka: {str(e)}")
            raise

# Convenience functions
def create_broker(
    broker_type: str,
    config: MessageConfig
) -> MessageBroker:
    """Create a message broker instance."""
    brokers = {
        "rabbitmq": RabbitMQBroker,
        "kafka": KafkaBroker
    }
    
    if broker_type not in brokers:
        raise ValueError(f"Unsupported broker type: {broker_type}")
        
    return brokers[broker_type](config) 