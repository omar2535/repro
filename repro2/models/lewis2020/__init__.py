import os

VERSION = "1.2"
MODEL_NAME = os.path.basename(os.path.dirname(__file__))
DOCKERHUB_REPO = f"danieldeutsch/{MODEL_NAME}"
DEFAULT_IMAGE = f"{DOCKERHUB_REPO}:{VERSION}"
AUTOMATICALLY_PUBLISH = True

from repro2.models.lewis2020.model import BART
from repro2.models.lewis2020.setup import Lewis2020SetupSubcommand
