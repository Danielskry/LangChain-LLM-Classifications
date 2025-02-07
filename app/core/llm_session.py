""" LLM session. """

from app.core.environment import get_environment
from app.config import config as app_config

def get_llm():
    """ Returns configurated LLM. """
    env = get_environment()
    return app_config[env].LLM.llm
