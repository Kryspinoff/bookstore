from dataclasses import dataclass
import os


@dataclass
class StaticFile:
    """
    Constants for the various path dirs
    """
    _base = os.path.dirname(os.path.abspath(__name__))
    _app = os.path.join(_base, "app")
    _static = os.path.join(_app, "static")
    files = os.path.join(_static, "files")
    files_books = os.path.join(files, "books")
    images = os.path.join(_static, "images")
    images_books = os.path.join(images, "books")
