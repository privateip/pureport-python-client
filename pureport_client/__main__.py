# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

import os
import sys
import glob
import shlex
import importlib

from click import (
    group,
    option,
    pass_context,
    version_option,
    Command,
    echo
)

import click

from pureport_client import __version__

from pureport_client.client import Client

from pureport_client.util import (
    construct_commands,
    find_client_commands
)


@group(context_settings={'auto_envvar_prefix': 'PUREPORT'})
@option('-u', '--api_url', help='The api url for this client.')
@option('-k', '--api_key', help='The API Key.')
@option('-s', '--api_secret', help='The API Key secret.')
@option('-p', '--api_profile', help='The API Profile if using file-based configuration.')
@option('-t', '--access_token', help='The API Key access token.')
@version_option()
@pass_context
def cli(ctx, api_url, api_key, api_secret, api_profile, access_token):
    """
    \f
    :param click.Context ctx:
    :param str api_url:
    :param str api_key:
    :param str api_secret:
    :param str api_profile:
    :param str access_token:
    """
    ctx.obj = Client(base_url=api_url,
                     key=api_key,
                     secret=api_secret,
                     profile=api_profile,
                     access_token=access_token)


def make(cli):
    # XXX: this function will dynamically discover the command tree based on
    # introspecting the Command class in each module.  By design the class
    # introspection is not more than two levels deep.  This will need to be
    # modified in the future, if more than two command levels are required.

    commands = list()

    for item in glob.glob(os.path.join(os.path.dirname(__file__), 'commands/*')):
        if os.path.isdir(item):
            name = item.split('/')[-1]

            if not name.startswith('_'):
                kwargs = {}

                kwargs['name'] = name.replace('_', '-')

                pkg = "pureport_client.commands.{}".format(name)
                mod = importlib.import_module(pkg)
                kwargs['context'] = mod.Command

                kwargs['commands'] = list()

                for item in find_client_commands(mod.Command):
                    try:
                        sub = importlib.import_module(".".join((pkg, item.__name__)))
                        kwargs['commands'].append({
                            'name': item.__name__.replace('_', '-'),
                            'context': getattr(mod.Command, item.__name__),
                            'commands': find_client_commands(sub.Command)
                        })
                    except ImportError:
                        kwargs['commands'].append(item)

                commands.append(kwargs)

    for command in construct_commands(commands):
        cli.add_command(command)


def run():
    make(cli)

    if len(sys.argv) == 1:
        shell()
    else:
        cli()


def shell():
    context = list()
    prompt = "> "
    mode = None

    echo("pureport cli {}".format(__version__))
    line = ''
    lineidx = 0
    history = list()

    while True:
        if context:
            prompt = "[edit {}]\r\n> ".format(' '.join(context))
        else:
            prompt = "> "
            mode = None

        echo('\r\n{}'.format(prompt), nl=False)

        while True:
            char = click.getchar(echo=True)

            import q
            q(char)
            if len(char) == 1:
                q(ord(char))

            # Up Arrow
            if char == '\x1b[A':
                echo('\r')
                echo(u'\u001b[1K', nl=False)
                echo(prompt, nl=False)
                lineidx -= 1
                if (lineidx * -1) >= len(history):
                    echo('\x07')  # bell alert
                    line = history[0]
                else:
                    line = history[lineidx]
                echo(line, nl=False)

            # ?
            elif ord(char) == 63:
                line = 'help'
                echo('\r')
                break

            # Control-C
            elif ord(char) == 3:
                sys.exit(1)

            # Arrow keys
            elif ord(char) == 27:
                import q; q.d()

            # Backspace
            elif ord(char) == 127:
                line = line[:-1]
                echo('\b', nl=False)
                echo(u'\u001b[0K', nl=False)

            # Enter
            elif ord(char) == 13:
                echo('\r')
                break

            elif 32 <= ord(char) <=126:
                line += char

        history.append(line)
        cmdline = shlex.split(line)
        line = ''
        lineidx = 0

        if not cmdline:
            continue

        elif cmdline[0].lower() in ('exit', 'quit'):
            sys.exit(0)

        elif cmdline[0].lower() == 'edit':
            context = cmdline[1:]
            mode = 'edit'

        elif cmdline[0].lower() == 'top':
            context = list()

        elif cmdline[0].lower() == 'up':
            if context:
                context.pop(-1)

        elif cmdline[-1].lower() == 'help':
            cmd = cli

            cmds = context.copy()
            cmds.extend(cmdline[:-1])

            for item in cmds:
                if isinstance(item, Command):
                    cmd = item
                    break
                cmd = cmd.commands.get(item)

            print("Possible completions")
            for key, value in cmd.commands.items():
                echo('  {:<25} {}\r'.format(key, value.help.strip()))

        elif mode == 'edit':
            echo(cmdline)

        else:
            try:
                command = context.copy()
                command.extend(cmdline)
                cli(command)
            except SystemExit as exc:
                pass

