from app.enums import StrEnum


class ProfileActiveStatusEnum(StrEnum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"

class ProfileStrategyModeEnum(StrEnum):
    LOADBALANCE = "loadbalance"
    FALLBACK = "fallback"
    RETRY = "retry"
    CACHING = "caching"
