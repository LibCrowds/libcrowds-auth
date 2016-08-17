# -*- coding: utf8 -*-
"""
LibCrowdsAuth
-------------

Modified authentication methods for LibCrowds.
"""

import os
import json
from flask import current_app as app
from flask.ext.plugins import Plugin

__plugin__ = "LibCrowdsAuth"
__version__ = json.load(open(os.path.join(os.path.dirname(__file__),
                                          'info.json')))['version']


class LibCrowdsAuth(Plugin):
    """Libcrowds auth plugin class."""

    def setup(self):
        """Setup the plugin."""
        from pybossa.auth import result
        result.ResultAuth._update = _update_result


def _update_result(self, user, result):
    """Allow project owner or admin to update results."""
    if user.is_anonymous():
        return False
    project = self._get_project(result, result.project_id)
    return (project.owner_id == user.id or user.admin)
