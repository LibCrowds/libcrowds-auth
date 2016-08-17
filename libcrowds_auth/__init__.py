# -*- coding: utf8 -*-
"""
LibCrowdsAuth
-------------

Modified authentication methods for LibCrowds.
"""

import os
import json
import default_settings
from flask import current_app as app
from flask.ext.plugins import Plugin

__plugin__ = "LibCrowdsAuth"
__version__ = json.load(open(os.path.join(os.path.dirname(__file__),
                                          'info.json')))['version']


class LibCrowdsAuth(Plugin):
    """Libcrowds auth plugin class."""

    def setup(self):
        """Setup the plugin."""
        self.load_config()
