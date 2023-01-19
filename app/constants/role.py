from enum import Enum


class Role(str, Enum):
    """
    Constants for the various roles scoped in the application ecosystem
    """

    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
