from dataclasses import dataclass


@dataclass(frozen=True)
class AgentConfig:
    ENABLED: bool = False
    RUN_INTERVAL: str = "12_hours"
    MAX_RETRY: int = 3
    TIMEOUT: int = 300
    LOG_LEVEL: str = "INFO"
    AMAZON_PA_API_KEY: str | None = None
    FLIPKART_AFFILIATE_API_KEY: str | None = None
    CUELINKS_API_KEY: str | None = None
    EARNKARO_API_KEY: str | None = None
    ADMITAD_API_KEY: str | None = None
    IMPACT_API_KEY: str | None = None
    OPENROUTER_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None

