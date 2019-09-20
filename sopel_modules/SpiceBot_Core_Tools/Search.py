# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot search system.
"""
import sopel

from sopel_modules.spicemanip import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('module')
@sopel.module.commands('search', 'find', 'google', 'lookup')
def search_main(bot, trigger, botcom):

    searchterm = spicemanip(botcom.dict['args'], 0) or None
    if not searchterm:
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "Not sure what you want me to look for.")
        return

    searchdict = {
                    "query": searchterm,
                    }

    searchreturn = SpiceBot.search.search(searchdict)
    if not searchreturn:
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], 'I cannot find anything about that')
    else:
        bot.osd(["[Information search for '" + str(searchterm) + "']", str(searchreturn)])


@SpiceBot.prerun('module')
@sopel.module.commands("where", "whereis")
def search_where(bot, trigger, botcom):

    searchterm = spicemanip(botcom.dict['args'], 0) or None
    if not searchterm:
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "Not sure what you want me to look for.")
        return
    searchdict = {
                    "query": searchterm,
                    "query_type": "maps",
                    }

    searchreturn = SpiceBot.search.search(searchdict)
    if not searchreturn:
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], 'I cannot find anything about that')
    else:
        bot.osd(["[Location search for " + str(searchterm) + "]", str(searchreturn)])


@SpiceBot.prerun('module')
@sopel.module.commands("what", "whatis")
def search_what(bot, trigger, botcom):

    searchterm = spicemanip(botcom.dict['args'], 0) or None
    if not searchterm:
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "Not sure what you want me to look for.")
        return
    searchdict = {
                    "query": searchterm,
                    }

    searchreturn = SpiceBot.search.search(searchdict)
    if not searchreturn:
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], 'I cannot find anything about that')
    else:
        bot.osd(["[Information search for '" + str(searchterm) + "']", str(searchreturn)])


@SpiceBot.prerun('module')
@sopel.module.commands("youtube", "video")
def search_video(bot, trigger, botcom):

    searchterm = spicemanip(botcom.dict['args'], 0) or None
    if not searchterm:
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "Not sure what you want me to look for.")
        return
    searchdict = {
                    "query": searchterm,
                    "query_type": "youtube",
                    }

    searchreturn = SpiceBot.search.search(searchdict)
    if not searchreturn:
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], 'I cannot find anything about that')
    else:
        bot.osd(["[Youtube search for '" + str(searchterm) + "']", str(searchreturn)])
