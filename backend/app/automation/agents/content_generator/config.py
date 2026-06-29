from app.automation.configs.agent_config import AgentConfig


ENABLED = False
RUN_INTERVAL = "weekly"
MAX_RETRY = 3
TIMEOUT = 300
LOG_LEVEL = "INFO"
AMAZON_PA_API_KEY = None
FLIPKART_AFFILIATE_API_KEY = None
CUELINKS_API_KEY = None
EARNKARO_API_KEY = None
ADMITAD_API_KEY = None
IMPACT_API_KEY = None
OPENROUTER_API_KEY = None
GROQ_API_KEY = None
OPENAI_API_KEY = None


def get_config() -> AgentConfig:
    return AgentConfig(**{key: value for key, value in globals().items() if key.isupper()})

