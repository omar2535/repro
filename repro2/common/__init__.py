import json
import os
from pathlib import Path

from repro2.common.checks import ConfigurationError
from repro2.common.registrable import Registrable
from repro2.common.tempdir import TemporaryDirectory

REPRO_CONFIG_FILE = os.getenv(
    "REPRO_CONFIG", default=Path.home() / ".repro/config.json"
)

if os.path.exists(REPRO_CONFIG_FILE):
    config = json.load(open(REPRO_CONFIG_FILE, "r"))
else:
    config = {}

REPRO_CONFIG = {
    "docker_server": config.pop("docker_server", "unix://var/run/docker.sock")
}
