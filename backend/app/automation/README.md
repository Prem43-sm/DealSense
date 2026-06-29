# DealSense Automation Framework

Phase 2.1 adds architecture for future autonomous workers without implementing AI, crawling, scraping, affiliate automation, or scheduled jobs.

## Architecture

```text
FastAPI
  |
  +-- /automation/status
        |
        +-- HealthService
              |
              +-- AutomationScheduler (idle)
                    |
                    +-- BaseAgent
                    |     +-- product_discovery
                    |     +-- price_monitor
                    |     +-- affiliate_manager
                    |     +-- availability_checker
                    |     +-- shopping_assistant
                    |     +-- content_generator
                    |
                    +-- Shared Services
                          +-- DatabaseService
                          +-- QueueService
                          +-- NotificationService
```

## Folder Structure

- `agents/`: Future workers grouped by responsibility.
- `common/`: Base agent lifecycle, logger, and scheduler framework.
- `configs/`: Shared configuration types.
- `services/`: Thin adapters around database, queue, notification, and health concerns.
- `logs/`: Per-agent log files are written here at runtime.

## Worker Lifecycle

Every worker inherits `BaseAgent` and receives dependencies through `AgentRuntime`:

- Database session or database service
- Agent logger
- Agent config
- Scheduler reference
- Shared services

The lifecycle methods are:

- `start()`
- `stop()`
- `run()`
- `health()`
- `status()`
- `log()`

Future agents should override only `run()`.

## Creating A New Agent

1. Create `backend/app/automation/agents/<agent_name>/`.
2. Add `agent.py`, `config.py`, `README.md`, and `__init__.py`.
3. Inherit from `BaseAgent`.
4. Add `config_factory = staticmethod(get_config)`.
5. The scheduler will discover the agent package automatically.

## Scheduler Flow

`AutomationScheduler` registers all agents and exposes supported intervals:

- `30_minutes`
- `1_hour`
- `6_hours`
- `12_hours`
- `daily`
- `weekly`

Phase 2.1 intentionally does not create APScheduler jobs. Actual scheduling should be added only when each worker has real, reviewed behavior.

## Future Roadmap

The framework is ready to accept adapters for:

- Amazon PA API
- Flipkart Affiliate API
- Cuelinks
- EarnKaro
- Admitad
- Impact
- OpenRouter
- Groq
- OpenAI
- Redis Queue
- Celery

## Coding Standards

- Reuse existing DealSense services and database modules.
- Inject dependencies into agents; avoid hidden runtime globals.
- Keep agents side-effect free until a future implementation phase.
- Add provider integrations behind services or adapters.
- Keep each agent responsible for one workflow.
- Do not duplicate current collectors, models, APIs, or schedulers.
