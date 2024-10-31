"""Example of event system usage."""
import asyncio
from pepperpy.events import (
    EventPriority,
    subscribe,
    publish,
    event_bus
)

# Event handlers
@subscribe("user.login", priority=EventPriority.HIGH)
async def log_login(event):
    """Log user login events."""
    print(f"🔐 User login: {event.data['username']} at {event.timestamp}")

@subscribe("user.login", priority=EventPriority.NORMAL)
async def send_welcome_message(event):
    """Send welcome message on login."""
    print(f"👋 Welcome back, {event.data['username']}!")

@subscribe("error", priority=EventPriority.CRITICAL)
async def handle_error(event):
    """Handle error events."""
    print(f"❌ Error occurred: {event.data['message']}")
    if 'traceback' in event.data:
        print(f"Traceback:\n{event.data['traceback']}")

async def demonstrate_events():
    """Demonstrate event system functionality."""
    # Start event processing
    await event_bus.start()
    
    try:
        # Publish login event
        await publish(
            "user.login",
            {
                "username": "john_doe",
                "login_time": "2024-03-20 10:00:00"
            }
        )
        
        # Simulate some error
        try:
            raise ValueError("Something went wrong!")
        except Exception as e:
            await publish(
                "error",
                {
                    "message": str(e),
                    "traceback": "..."
                },
                priority=EventPriority.CRITICAL
            )
        
        # Wait for events to be processed
        await asyncio.sleep(1)
        
    finally:
        # Stop event processing
        await event_bus.stop()

def main():
    """Run the demonstration."""
    asyncio.run(demonstrate_events())

if __name__ == "__main__":
    main() 