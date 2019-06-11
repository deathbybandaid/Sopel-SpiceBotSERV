# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot

import spicemanip


@sopel.module.rule('(.*)')
def bot_command_rule(bot, trigger):

    # TODO add config limits
    # but still allow in privmsg

    if trigger.nick == bot.nick:
        return

    if not len(trigger.args):
        return

    message = trigger.args[1]
    message = ''.join([x for x in message if ord(x) < 128])

    # ignore text coming from a valid prefix
    if str(message).startswith(tuple(bot.config.core.prefix_list)):
        return
        trigger_args, trigger_command = SpiceBot.prerun.trigger_args(message, 'module')
        # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
        if trigger_command.startswith("."):
            return
        commands_list = []
        for commandstype in list(SpiceBot.commands.dict['commands'].keys()):
            if commandstype not in ['rule', 'nickname']:
                for com in list(SpiceBot.commands.dict['commands'][commandstype].keys()):
                    if com not in commands_list:
                        commands_list.append(com)
        if trigger_command not in commands_list:
            if not SpiceBot.letters_in_string(trigger_command):
                return
            invalid_display = ["I don't seem to have a command for " + str(trigger_command) + "!"]
            # invalid_display.append("If you have a suggestion for this command, you can run .feature ." + str(trigger_command))
            # invalid_display.append("ADD DESCRIPTION HERE!")
            bot.osd(invalid_display, trigger.nick, 'notice')
        return

    if str(message).lower().startswith(str(bot.nick).lower()):
        command_type = 'nickname'
        trigger_args, trigger_command = SpiceBot.prerun.trigger_args(message, 'nickname')
        trigger_args.insert(0, trigger_command)
        fulltrigger = spicemanip.main(trigger_args, 0)
        if str(trigger_command).startswith("?"):
            return
        if fulltrigger in SpiceBot.commands.dict['nickrules']:
            return
        if trigger_command in list(SpiceBot.commands.dict['commands']["nickname"].keys()):
            return
    else:
        command_type = 'other'
        trigger_args = spicemanip.main(message, 'create')
        trigger_command = trigger_args[0]
        fulltrigger = spicemanip.main(trigger_args, 0)

    returnmessage = SpiceBot.botai.on_message(bot, trigger, message)
    if returnmessage:
        bot.osd(str(returnmessage))
    else:
        if command_type == 'nickname':

            if trigger_args[0].lower() in ["what", "where"] and trigger_args[1].lower() in ["is", "are"]:
                # TODO saved definitions
                searchterm = spicemanip.main(trigger_args, "3+") or None
                if searchterm:
                    if trigger_args[0].lower() == "where":
                        searchreturn = SpiceBot.googlesearch(searchterm, 'maps')
                    else:
                        searchreturn = SpiceBot.googlesearch(searchterm)
                    if not searchreturn:
                        bot.osd('I cannot find anything about that')
                    else:
                        bot.osd(str(searchreturn))
                return

            elif trigger_args[0].lower() in ["can"] and trigger_args[1].lower() in ["you"] and trigger_args[2].lower() in ["see"]:
                target = spicemanip.main(trigger_args, "4+") or None
                if target:
                    if SpiceBot.inlist(trigger.nick, bot.users):
                        realtarget = SpiceBot.inlist_match(target, bot.users)
                        dispmsg = [trigger.nick + ", yes. I can see " + realtarget]
                        targetchannels = []
                        for channel in list(bot.channels.keys()):
                            if SpiceBot.inlist(trigger.nick, list(bot.channels[channel].privileges.keys())):
                                targetchannels.append(channel)
                        dispmsg.append(realtarget + " is in " + spicemanip.main(targetchannels, 'andlist'))
                        bot.osd(dispmsg)
                    else:
                        bot.osd(trigger.nick + ", no. I cannot see " + target + " right now!")
                        # if bot_check_inlist(target, list(bot.memory["botdict"]["users"].keys())):
                        #    bot.osd(trigger.nick + ", I can't see " + inlist_match(target, bot.users) + " at the moment.")
                        # else:
                        #    bot.osd("I have never seen " + str(target) + ".")
                        # user in list(bot.channels[channel].privileges.keys())
                        # TODO
                return

            elif fulltrigger.lower().endswith("order 66"):

                if fulltrigger.lower() == "execute order 66":
                    if SpiceBot.inlist(trigger.nick, SpiceBot.bot_privs('owners')):
                        if trigger.is_privmsg:
                            jedi = None
                        else:
                            jedilist = list(bot.channels[trigger.sender].privileges.keys())
                            for nonjedi in [bot.nick, trigger.nick]:
                                if nonjedi in jedilist:
                                    jedilist.remove(nonjedi)
                            jedi = spicemanip.main(jedilist, 'random')

                        if jedi:
                            bot.osd("turns to " + jedi + " and shoots him.", trigger.sender, 'action')
                        else:
                            bot.osd(" cannot find any jedi nearby.", trigger.sender, 'action')
                    else:
                        bot.osd("I'm sure I don't know what you're talking about.")

                elif fulltrigger.lower() == "explain order 66":
                    if SpiceBot.inlist(trigger.nick, SpiceBot.bot_privs('owners')):
                        bot.osd("Order 66 is an instruction that only you can give, sir. When you give the order I will rise up against the jedi and slay them.")
                    else:
                        bot.osd("I'm afraid I cannot tell you that, sir.")
                else:
                    bot.osd("I'm sure I don't know what you're talking about.")
                return

            elif fulltrigger.lower().startswith(tuple(["make me a", "beam me a"])):
                makemea = spicemanip.main(trigger.sb['args'], "4+") or None
                if makemea:
                    bot.osd("beams " + trigger.nick + " a " + makemea, trigger.sender, 'action')
                else:
                    bot.osd(trigger.nick + ", what would you like me to beam you?")
                return

            elif fulltrigger.lower().startswith("beam me to"):
                location = spicemanip.main(trigger.sb['args'], "4+") or None
                if location:
                    bot.osd("locks onto " + trigger.nick + "s coordinates and transports them to " + location, 'action')
                else:
                    bot.osd(trigger.nick + ", where would you like me to beam you?")
                return

            elif fulltrigger.lower() == "initiate clean slate protocol":
                if SpiceBot.inlist(trigger.nick, SpiceBot.bot_privs('admins')):
                    bot.osd("sends a destruct command to the network of bots.", 'action')
                else:
                    bot.osd("I'm afraid you do not have the authority to make that call, " + trigger.nick + ".")
                return

            # elif fulltrigger.lower().startswith("what time is it"):
            # TODO

            # elif fulltrigger.lower().startswith(tuple(["have you seen"])):
            #    posstarget = spicemanip.main(trigger.sb['args'], 4) or 0
            #    message = seen_search(bot, botcom, posstarget)
            #    bot.osd(message)
            #    return
            # TODO

            closestmatches = SpiceBot.similar_list(trigger_command, list(SpiceBot.commands.dict['commands']["nickname"].keys()), 3, 'reverse')
            if len(closestmatches):
                closestmatches = spicemanip.main(closestmatches, "andlist")
                bot.osd("I don't know what you are asking me to do! Did you mean: " + str(closestmatches) + "?")
                return
            else:
                bot.osd("I don't know what you are asking me to do!")
                return
