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

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./automation.db")