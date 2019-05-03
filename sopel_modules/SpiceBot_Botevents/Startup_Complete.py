# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.tools import stderr

from .BotEvents import set_bot_event, check_bot_startup


@sopel.module.event('001')
@sopel.module.rule('.*')
def bot_startup_complete(bot, trigger):

    while not check_bot_startup(bot):
        pass

    set_bot_event(bot, "startup_complete")
    stderr("[Sopel_BotEvents] Module Events Logging Complete")
