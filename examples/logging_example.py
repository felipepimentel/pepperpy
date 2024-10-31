"""Example of enhanced logging capabilities."""
from pepperpy.logging import get_logger, LogConfig, LogStyle

def demonstrate_logging():
    # Basic usage
    logger = get_logger()
    
    logger.debug("🔍 Detailed debug information")
    logger.info("ℹ️ Normal operation message")
    logger.success("✅ Operation completed successfully")
    logger.warning("⚠️ Warning about potential issues")
    logger.error("❌ Error that needs attention")
    logger.critical("🚨 Critical system failure")
    
    # Custom styling
    custom_style = LogStyle(
        time_color="blue",
        level_colors={
            "DEBUG": "magenta",
            "INFO": "cyan",
            "SUCCESS": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold red"
        },
        metadata_color="white"
    )
    
    styled_logger = get_logger("styled", style=custom_style)
    styled_logger.info("🎨 Using custom styling")
    
    # Contextualized logging
    user_logger = get_logger("user_service", user_id="123", role="admin")
    user_logger.info("👤 User logged in successfully")
    
    # Custom configuration
    custom_config = LogConfig(
        console_level="DEBUG",
        file_enabled=True,
        rotation="1 day",
        style=LogStyle(
            time_format="HH:mm:ss",
            message_same_as_level=False
        )
    )
    
    custom_logger = get_logger("custom", config=custom_config)
    custom_logger.info("⚙️ Using custom configuration")
    
    # Error handling
    try:
        raise ValueError("Invalid input")
    except Exception as e:
        logger.exception("❌ Operation failed")

if __name__ == "__main__":
    demonstrate_logging() 