from typing import Any


class NotificationService:
    def send(self, channel: str, payload: dict[str, Any]) -> None:
        # Placeholder adapter for email, webhooks, Slack, or push providers.
        return None

