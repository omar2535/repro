import os

VERSION = "1.0"
MODEL_NAME = os.path.basename(os.path.dirname(__file__))
DOCKERHUB_REPO = f"danieldeutsch/{MODEL_NAME}"
DEFAULT_IMAGE = f"{DOCKERHUB_REPO}:{VERSION}"
AUTOMATICALLY_PUBLISH = True

from repro2.models.colombo2021.models import DepthScore, BaryScore, InfoLM
from repro2.models.colombo2021.setup import Colombo2021SetupSubcommand
