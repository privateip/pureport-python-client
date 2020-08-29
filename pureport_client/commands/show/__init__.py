# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from __future__ import absolute_import

from click import (
    option,
    argument
)

from pureport_client.commands import CommandBase


class Command(CommandBase):
    """Show system information
    """

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def networks(self, account_id):
        """Display all networks for the provided account

        \f
        :returns: a list of Network objects
        :rtype: list
        """
        return self.__call__('get', '/accounts/{}/networks'.format(account_id))

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def connections(self, account_id):
        """Display a list of all account connections

        \f
        :returns: a list of connection objects
        :rtype: list
        """
        return self.__call__('get', '/accounts/{}/connections'.format(account_id))

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def api_keys(self, account_id):
        """Get a list of all API keys for an account.

        \f
        :returns: list of account objects
        :rtype: list
        """
        return self.__call__('get', '/accounts/{}/apikeys'.format(account_id))

    @option('-a', '--account_id', envvar='PUREPORT_ACCOUNT_ID', required=True)
    def roles(self, account_id):
        """Display all roles for the provided account

        \f
        :returns: a list of AccountRole objects
        :rtype: list
        """
        return self.__call__('get', '/accounts/{}/roles'.format(account_id))


