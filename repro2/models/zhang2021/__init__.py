import os

VERSION = "1.2"
MODEL_NAME = os.path.basename(os.path.dirname(__file__))
DOCKERHUB_REPO = f"danieldeutsch/{MODEL_NAME}"
DEFAULT_IMAGE = f"{DOCKERHUB_REPO}:{VERSION}"
AUTOMATICALLY_PUBLISH = True

from repro2.models.zhang2021.model import Lite3Pyramid
from repro2.models.zhang2021.setup import Zhang2021SetupSubcommand
