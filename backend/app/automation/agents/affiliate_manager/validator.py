from enum import StrEnum
from urllib.parse import urlparse


class ValidationStatus(StrEnum):
    VALID = "VALID"
    INVALID = "INVALID"
    UNKNOWN = "UNKNOWN"


class AffiliateLinkValidator:
    def validate(self, *, provider: str, url: str | None) -> ValidationStatus:
        if not url:
            return ValidationStatus.INVALID

        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            return ValidationStatus.INVALID

        if provider.lower() not in parsed.netloc.lower() and provider.lower() not in parsed.query.lower():
            return ValidationStatus.UNKNOWN

        return ValidationStatus.VALID

