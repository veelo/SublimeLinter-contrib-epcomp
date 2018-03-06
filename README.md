SublimeLinter-contrib-epcomp
================================

[![Build Status](https://travis-ci.org/veelo/SublimeLinter-contrib-epcomp.svg?branch=master)](https://travis-ci.org/veelo/SublimeLinter-contrib-epcomp)

This linter plugin for [SublimeLinter][docs] provides an interface to `epcomp`, the [Prospero Extended Pascal][prospero] 3.2 compiler. It will be used with files that have the “pascal” syntax.

## Installation
SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here][installation].

### Linter installation
Before using this plugin, you must ensure that [Prospero Extended Pascal][prospero] is installed on your system. Currently it is not easy to get hold of this legacy commercial compiler, but if you are interested in this linter, you probably already have access to it. The compiler does the linting.


**Note:** This plugin requires `epcomp` from Prospero Extended Pascal v3.2.07 or later.

### Linter configuration
In order for `epcomp` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. This can be done in two ways:

1. Read and follow the steps in [“Finding a linter executable”](http://sublimelinter.readthedocs.org/en/latest/troubleshooting.html#finding-a-linter-executable) through “Validating your PATH” in the documentation. Or:

1. Select `Preferences -> Package Settings -> SublimeLinter -> Settings` and insert the `executable` setting in the right pane, similar to:


        "linters": {
            "epcomp": {
                "executable": "C:\\extpas32\\bin\\epcomp.exe"
            }
        }

    Note the use of escaped backslashes. Trailing backslashes are optional. Restart Sublime Text for this setting to take effect.

Once you have installed and configured `epcomp`, you can proceed to install the SublimeLinter-contrib-epcomp plugin if it is not yet installed.

### Plugin installation
Please use [Package Control][pc] to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, see [Contributing](#contributing).

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette][cmd] and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `epcomp`. Among the entries you should see `SublimeLinter-contrib-epcomp`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings
For general information on how SublimeLinter works with settings, please see [Settings][settings]. For information on generic linter settings, please see [Linter Settings][linter-settings].

In addition to the standard SublimeLinter settings, SublimeLinter-contrib-epcomp provides its own settings.

|Setting|Description|Inline Setting|
|:------|:----------|:------------:|
|ignore |Ignore warnings. Supported values: `"possible-unclosed-comment"` or error codes like: `["282", "283"]`.|&#10003;|

### Implementing per-project settings
Typically you will want to configure the linter with the same options as the compiler, on a per-project basis. This can be conveniently accomplished in your project settings using [Settings Tokens][settings-tokens].

For example, let’s say the interface files of your project are in the subdirectory `source\obj`, *and* you want to suppress warnings about possible unclosed comments:

* If you have not already created a project in Sublime Text, select `Project -> Save Project As...`.

* Select `Project -> Edit Project`.

* At the **top** level of the project’s JSON data, add the following:

        "SublimeLinter":
        {
            "linters":
            {
                "epcomp":
                {
                    "args": [
                        "-i${project_path}\\source\\obj",
                        "-o${project_path}\\source\\obj"
                    ],
                    "ignore": "possible-unclosed-comment"
                }
            }
        }

* Save the file.

Any time you edit the project and change a linter’s settings, all open files that use that linter will be re-linted to reflect the new settings.

### Ignoring warnings per-file

The message `Warning: possible unclosed comment` can be ignored on a global or project level with the following setting:

    "ignore": "possible-unclosed-comment"

The same can be accomplished per individual file by adding the following line in your code:

    {[SublimeLinter epcomp-ignore:possible-unclosed-comment]}

 or

    {[SublimeLinter epcomp-ignore:282]}


## Contributing
If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Clone it into Packages (on Windows: `C:\Users\<user>\AppData\Roaming\Sublime Text 3\Packages`).
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make a pull request.

You may want to consult the documentation for [creating a linter plugin][creating-linter-plugin].
Please note that modifications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbreviations unless they are very well known.

Thank you for helping out!

[prospero]: https://web.archive.org/web/20050305055139/http://www.prosperosoftware.com/e32iw.html
[docs]: http://sublimelinter.readthedocs.org
[installation]: http://sublimelinter.readthedocs.org/en/latest/installation.html
[locating-executables]: http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located
[pc]: https://sublime.wbond.net/installation
[cmd]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
[settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html
[linter-settings]: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
[inline-settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html#inline-settings
[settings-tokens]: http://www.sublimelinter.com/en/latest/settings.html#settings-tokens
[creating-linter-plugin]: http://sublimelinter.readthedocs.io/en/latest/linter_plugin.html
