import enum


class PeriodType(str, enum.Enum):
    MONTH = "Месяц"
    HALF_YEAR = "Полгода"
    YEAR = "Год"

class SubscriptionType(str, enum.Enum):
    MINUTE = "Минутный"
    UNLIMITED = "Безлимитный"