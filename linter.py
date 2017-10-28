#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Bastiaan Veelo
# Copyright (c) 2016-2017 Bastiaan Veelo
#
# License: MIT
#

"""This module exports the Epcomp plugin class."""

from SublimeLinter.lint import Linter, util, persist
from functools import lru_cache
import re


class Epcomp(Linter):
    """Provides an interface to epcomp, the Prospero Extended Pascal compiler."""

    syntax = 'pascal'
    cmd = 'epcomp.exe'
    regex = r'''(?xi)
        # The first line contains the line number, error code (stored in P<warning>) and message
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
    @lru_cache(maxsize=None)
    def can_lint(cls, syntax):
        """
        Determine if the linter can handle the provided syntax.
        This is an optimistic determination based on the linter's syntax alone.
        """

        can = False
        syntax = syntax.lower()

        if cls.syntax:
            if isinstance(cls.syntax, (tuple, list)):
                can = syntax in cls.syntax
            elif cls.syntax == '*':
                can = True
            elif isinstance(cls.syntax, str):
                can = syntax == cls.syntax
            else:
                can = cls.syntax.match(syntax) is not None

        return can

    def context_sensitive_executable_path(self, cmd):
        """
        Calculate the context-sensitive executable path, return a tuple of (have_path, path).
        """

        global_cmd = util.which(cmd[0])
        if global_cmd:
            return True, global_cmd

        local_cmd = None
        epbin = self.get_view_settings().get('epbin', None)
        if epbin is not None:
            if epbin[-1:] is "\\":
                local_cmd = epbin + cmd[0]
            else:
                local_cmd = epbin + "\\" + cmd[0]
        if util.can_exec(local_cmd):
            return True, local_cmd

        persist.printf(
            'WARNING: {} deactivated, cannot locate {} in path or in {}'
            .format(self.name, cmd[0], epbin)
        )
#        return False, cmd
        return True, None

    def build_cmd(self, cmd=None):
        """Return a tuple with the command line to execute."""

        result = super().build_cmd(cmd) or self.cmd + ['-y']
        if "options" in self.get_view_settings():
            for option in self.get_view_settings()["options"]:
                result += [option.replace('/', '\\')]
        return result

    def split_match(self, match):
        """Extract and return values from match. We override this method to give more precise feedback."""

        match, line, col, error, warning, message, near = super().split_match(match)

        # Strip the cr at the end of message:
        message = message[:-1]
        if near is not None:
            message = message + ': ' + near[:-1]
        near = None

        if "ignore" in self.get_view_settings():
            if self.get_view_settings()["ignore"] == warning:
                match = ''
            if self.get_view_settings()["ignore"] == "possible-unclosed-comment" and warning == '282':
                match = ''

        # col marks the end of the word, error contains the complete line of code.
        # Use this to find the beginning of the word.
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
            # We could remove the Warning word, but the Linter status line still reports it as "error", so leave it in.
            # message = message[9:]
        else:
            warning = ''

        return match, line, col, error, warning, message, near
