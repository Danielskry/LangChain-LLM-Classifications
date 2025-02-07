import logging
import logging.config
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import config as app_config
from app.core.environment import get_environment
from app.core.logger import get_logger

from app.utils.file_system_utils import create_directory

from app.routers.status_router import status_router
from app.routers.incident_router import incident_router

def create_app() -> FastAPI:
    """
    Create and configure an instance of the FastAPI application.

    This function initializes the FastAPI application, configures logging, registers
    routers, and sets up middleware based on the current application environment.

    Returns:
        FastAPI: The initialized FastAPI application instance.

    Raises:
        Exception: If an error occurs during the application initialization.
    """
    try:
        APP_ENVIRONMENT = get_environment()

        # Register logging
        logger = get_logger(__name__)
        register_logging(logger, APP_ENVIRONMENT)

        app = FastAPI(
            title=app_config[APP_ENVIRONMENT].APP_NAME,
            version=app_config[APP_ENVIRONMENT].APP_VERSION,
            docs_url=None if APP_ENVIRONMENT == "production" else "/docs",
            redoc_url=None if APP_ENVIRONMENT == "production" else "/redoc",
        )

        # Register routers
        init_routers(app, logger)

        # Make middleware
        make_middleware(app, logger, APP_ENVIRONMENT)

        logger.info("Completed initializing FastAPI app!")
        return app
    except Exception as e:
        logger.error(f"An error occurred during app initialization: {e}")
        raise

def init_routers(
    app_: FastAPI,
    logger: logging.Logger
) -> None:
    """
    Register routers with the FastAPI application.

    This function includes various routers (status, auth, query, file) in the FastAPI
    application for handling different routes.

    Args:
        app_ (FastAPI): The FastAPI application instance.
        logger (logging.Logger): The logger instance for logging.

    Raises:
        ImportError: If an error occurs while importing or including routers.
    """
    try:
        app_.include_router(status_router)
        app_.include_router(incident_router)
        logger.info("Registered routes for app!")
    except ImportError as e:
        logger.error(f"Error registering routes: {e}")
        raise


def make_middleware(
    app_: FastAPI,
    logger: logging.Logger,
    environment: str
) -> None:
    """
    Configure middleware for the FastAPI application.

    This function adds middleware to the FastAPI application, such as CORS middleware,
    based on the application configuration for the current environment.

    Args:
        app_ (FastAPI): The FastAPI application instance.
        logger (logging.Logger): The logger instance for logging.
        environment (str): The current application environment.

    Raises:
        ImportError: If an error occurs while adding middleware.
    """
    try:
        app_.add_middleware(
            CORSMiddleware,
            allow_origins=app_config[environment].CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=app_config[environment].ALLOWED_METHODS,
            allow_headers=app_config[environment].ALLOWED_HEADERS,
        )
        logger.info("Completed making middleware!")
    except ImportError as e:
        logger.error(f"An error occurred during making of middleware: {e}")
        raise

def register_logging(
    logger: logging.Logger,
    environment: str
) -> None:
    """
    Configure logging for the application.

    This function sets up logging based on the application configuration for the current
    environment, and ensures the log directory exists.

    Args:
        logger (logging.Logger): The logger instance for logging.
        environment (str): The current application environment.

    Raises:
        Exception: If an error occurs while registering logging configuration.
    """
    try:
        logging.config.dictConfig(app_config[environment].LOGGING)
        log_directory_path = os.environ.get("APP_LOGGING_DIR") or "logs"
        create_directory("", log_directory_path)

        logger.info("Logging configuration was successfully registered.")
        logger.info(f"Directory for logging created at: {log_directory_path}")
    except Exception as e:
        logger.error(
            f"An error occurred while registering logging configuration: {e}"
        )
        raise
