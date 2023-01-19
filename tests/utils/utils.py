import logging
import os
import random
import string

from app import schemas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.join(os.path.abspath(__name__))
TESTS_DIR = os.path.join(BASE_DIR, "tests")
DATA_DIR = os.path.join(TESTS_DIR, "data")
DOWNLOAD_DIR = os.path.join(DATA_DIR, "download")
UPLOAD_DIR = os.path.join(DATA_DIR, "upload")
IMAGE_PATH = os.path.join(UPLOAD_DIR, "1.jpg")
PDF_PATH = os.path.join(UPLOAD_DIR, "full book.pdf")
SHORT_PDF_PATH = os.path.join(UPLOAD_DIR, "short book.pdf")


# Settings field of schema
class SettingsField:
    def __init__(self, schema, field: str):
        self.name = field
        self.title = schema.schema().get("title")
        self.schema_data = schema.schema()

        self.properties = self.schema_data.get("properties")
        if not self.properties:
            raise ValueError(f"Fields doesn't exists in {self.title}")

        self.field = self.properties.get(self.name)
        if not self.field:
            raise ValueError(f"{self.name} field doesn't exists in {self.title}")

    @property
    def min_length(self):
        return self.field.get("minLength")

    @property
    def max_length(self):
        return self.field.get("maxLength")


def random_string(length) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


def random_lower_string_(length) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_integer(a, b) -> int:
    return random.randint(a, b)


def random_float(a, b) -> float:
    return random.uniform(a, b)


def random_valid_integer(field, schema) -> str:
    pattern = SettingsField(field, schema)
    length = random.randint(pattern.min_length, pattern.max_length)
    return random_string(length)


def random_valid_email() -> str:
    return f"{random_lower_string_(32)}@{random_lower_string_(32)}.com"


def random_valid_username() -> str:
    pattern = SettingsField(schemas.UserCreate, "username")
    length = random.randint(pattern.min_length, pattern.max_length)
    return f"{random_string(length)}"


def random_valid_password() -> str:
    pattern = SettingsField(schemas.UserCreate, "password")
    length = random.randint(pattern.min_length, pattern.max_length)
    total_characters = string.digits + string.ascii_letters + r"""!@#$%^&*()_-=+[{]};:'",<.>/?\|"""
    return "".join(random.choices(total_characters, k=length))


def random_valid_first_name() -> str:
    pattern = SettingsField(schemas.UserCreate, "first_name")
    length = random.randint(pattern.min_length, pattern.max_length)
    return random_string(length).title()


def random_valid_last_name() -> str:
    pattern = SettingsField(schemas.UserCreate, "last_name")
    length = random.randint(pattern.min_length, pattern.max_length)
    return random_string(length).title()


def random_valid_phone_number() -> str:
    pattern = SettingsField(schemas.UserCreate, "phone_number")
    length = random.randint(pattern.min_length, pattern.max_length)
    return "".join(random.choices(string.digits, k=length))
