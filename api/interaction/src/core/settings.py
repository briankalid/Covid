import os
import ast
from loguru import logger as logger_loguru
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class AppConfig:

    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.PROJECT_NAME="Interaction"
        self.API_V1="/v1"

        self.COUNTRIES=ast.literal_eval(os.getenv("COUNTRIES","[]"))
        self.AWS_ENPOINT_URL=os.getenv("AWS_ENPOINT_URL", None)


settings = AppConfig()