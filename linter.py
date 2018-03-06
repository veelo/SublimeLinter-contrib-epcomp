#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Bastiaan Veelo
# Copyright (c) 2016-2018 Bastiaan Veelo
#
# License: MIT
#

"""This module exports the Epcomp plugin class."""

from SublimeLinter.lint import Linter, util
import re

import logging

logger = logging.getLogger(__name__)


class Epcomp(Linter):
    """Provides an interface to the Prospero Extended Pascal compiler."""

    syntax = 'pascal'
    cmd = 'epcomp.exe -y'
    regex = r'''(?xi)
        # The first line contains the line number,
        # error code (stored in P<warning>) and message.
        ^\s*(?P<line>\d+)\s+(?P<warning>\d+)\s+(?P<message>.+)$\r?\n

        # Maybe extra info follows, preceded by 24 spaces. Record it in P<near>
        (^\s{24}(?P<near>.+)$\r?\n)?

        # The offending code. Record it in P<error>
        ^(?P<error>.*)$\r?\n

        # The column indication
        ^(?P<col>[ ]*)\^
    '''
    multiline = True
    tempfile_suffix = 'pas'
    error_stream = util.STREAM_STDOUT
    defaults = {
        'ignore': []
    }
    inline_settings = ('ignore')
    comment_re = r'\s*[{]'

    @classmethod
    def can_lint(cls):
            """Assume the linter can lint."""
            return True

    def split_match(self, match):
        """
        Extract and return values from match.

        We override this method to give more precise feedback.
        """
        match, line, col, error, warning, message, near = \
            super().split_match(match)

        # Strip the cr at the end of message:
        message = message[:-1]
        if near is not None:
            message = message + ': ' + near[:-1]
        near = None

        if "ignore" in self.get_view_settings():
            if self.get_view_settings()["ignore"] == warning:
                match = ''
            if warning in self.get_view_settings()["ignore"]:
                match = ''
            if self.get_view_settings()["ignore"] == \
                    "possible-unclosed-comment" and warning == '282':
                match = ''

        # col marks the end of the word, error contains the complete line of
        # code. Use this to find the beginning of the word.
        # col = error[:col].rfind(' ') + 1
        m = re.match(r'.*\W([a-zA-z0-9_]+)$', error[:col])
        if m:
            col = m.start(1)
        # else:
        #     col = 0

        # Color code the warnings as warning.
        if message.startswith('Warning:'):
            error = ''
            warning = message
            # We could remove the Warning word, but the Linter status line
            # still reports it as "error", so leave it in.
            # message = message[9:]
        else:
            warning = ''

        return match, line, col, error, warning, message, near
