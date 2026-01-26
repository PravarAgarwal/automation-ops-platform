'''
Docstring for app.config
This file answers:

“Where do settings live?”

Examples:
DB URL
Secret keys
Environment variables

Why separate?

Different environments:
Local
Test

Production
You never hardcode secrets.
This is critical in real systems.
'''

import os
import logging

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./automation.db")

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
)

logger = logging.getLogger("automation-platform")