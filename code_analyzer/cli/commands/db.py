"""Database management commands."""
import click
from loguru import logger
from code_analyzer.crews.models.base import init_db
from alembic import command
from alembic.config import Config

@click.group()
def db():
    """Database management commands."""
    pass

@db.command()
def init():
    """Initialize the database."""
    try:
        # Initialize database
        init_db()
        logger.info("✅ Database initialized")
        
        # Run migrations
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("✅ Migrations completed")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise click.ClickException(str(e))

@db.command()
def reset():
    """Reset the database."""
    try:
        alembic_cfg = Config("alembic.ini")
        command.downgrade(alembic_cfg, "base")
        command.upgrade(alembic_cfg, "head")
        logger.info("✅ Database reset completed")
        
    except Exception as e:
        logger.error(f"❌ Database reset failed: {e}")
        raise click.ClickException(str(e)) 