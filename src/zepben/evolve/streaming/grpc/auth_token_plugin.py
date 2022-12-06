#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import grpc
from zepben.auth import ZepbenTokenFetcher

__all__ = ["AuthTokenPlugin"]

_AUTH_HEADER_KEY = 'Authorization'


class AuthTokenPlugin(grpc.AuthMetadataPlugin):
    """
    Metadata plugin that injects tokens into the metadata of each call.
    Tokens are fetched using a provided :class:`ZepbenTokenFetcher`.
    """

    def __init__(self, token_fetcher: ZepbenTokenFetcher):
        self.token_fetcher = token_fetcher

    def __call__(self, context, callback):
        callback(((_AUTH_HEADER_KEY, self.token_fetcher.fetch_token()),), None)
