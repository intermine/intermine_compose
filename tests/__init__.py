"""Test suite for the Compose."""

import os

if os.environ.get("CI", False):
    os.environ["APP_CONFIG"] = "CI"
else:
    os.environ["APP_CONFIG"] = "TEST"
