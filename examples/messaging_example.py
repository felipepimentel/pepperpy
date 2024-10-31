"""Example of messaging system usage."""
import asyncio
import uuid
from pepperpy.messaging import (
    create_broker,
    MessageConfig,
    Message
)

async def handle_message(message: Message):
    """Handle received messages."""
    print(f"Received message: {message.content}")
    print(f"Message ID: {message.message_id}")
    print(f"Timestamp: {message.timestamp}")
    print(f"Headers: {message.headers}")
    print("---")

async def demonstrate_rabbitmq():
    """Demonstrate RabbitMQ messaging."""
    # Configure RabbitMQ
    config = MessageConfig(
        broker_url="amqp://guest:guest@localhost/",
        queue_name="demo_queue",
        exchange="demo_exchange",
        routing_key="demo.key"
    )
    
    # Create broker
    broker = create_broker("rabbitmq", config)
    await broker.connect()
    
    try:
        # Start consumer
        await broker.subscribe(handle_message)
        
        # Publish messages
        for i in range(5):
            message = Message(
                content=f"Test message {i}",
                message_id=str(uuid.uuid4()),
                headers={"sequence": i}
            )
            await broker.publish(message)
            print(f"Published message {i}")
            await asyncio.sleep(1)
            
        # Wait for messages to be processed
        await asyncio.sleep(5)
        
    finally:
        await broker.disconnect()

async def demonstrate_kafka():
    """Demonstrate Kafka messaging."""
    # Configure Kafka
    config = MessageConfig(
        broker_url="localhost:9092",
        queue_name="demo_topic"
    )
    
    # Create broker
    broker = create_broker("kafka", config)
    await broker.connect()
    
    try:
        # Start consumer
        await broker.subscribe(handle_message)
        
        # Publish messages
        for i in range(5):
            message = Message(
                content=f"Kafka message {i}",
                message_id=str(uuid.uuid4()),
                headers={"sequence": i}
            )
            await broker.publish(message)
            print(f"Published Kafka message {i}")
            await asyncio.sleep(1)
            
        # Wait for messages to be processed
        await asyncio.sleep(5)
        
    finally:
        await broker.disconnect()

async def main():
    """Run messaging demonstrations."""
    print("RabbitMQ Demo:")
    await demonstrate_rabbitmq()
    
    print("\nKafka Demo:")
    await demonstrate_kafka()

if __name__ == "__main__":
    asyncio.run(main()) 