import re
import logging


# Class contains some abstract parts but is not declared
# as an abstract base class (ABC) so that users can choose
# to simply implement the portions they want/need.
class CommandParser:
    class Error(Exception):
        pass

    def is_cmd(self, body):
        return body.lstrip().startswith(":")

    def process_command(self, from_num, to_num, body, time):
        # The +" " avoids errors when no args are provided
        cmd, args = (body.lstrip(' :').lower()+" ").split(' ', 1)

        method_name = '_cmd_{}'.format(cmd)

        try:
            # Split get and call
            # Otherwise we catch AttributeErrors from inside the call
            method = getattr(self, method_name)
        except AttributeError:
            return self._error("Unknown command '{}'".format(cmd))

        try:
            return method(args, from_num, to_num, body, time)
        except CommandParser.Error as e:
            return self._error("Cmd {}, {}".format(cmd, e))
        except NotImplementedError as e:
            return self._error("Cmd {}, {} not implemented".format(cmd, e))
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return self._error("Cmd {}, {}".format(cmd, "suffered from an unexpected server error.\nIf the problem persists please contact your administrator with details."))


    def _error(self, details):
            return "Error: '{}'\nTry :help for details on how to use the system.".format(details)

    def _cmd_help(self, args, from_num, to_num, body, time):
        # :help
        return "\n".join(
            ":transfer <phone number>",
            ":transfer <name>",
            ":transfer",
            ":",
            ":keep",
            ":current",
            ":help",
            ":source",
        )

    def _cmd_source(self, args, from_num, to_num, body, time):
        # :source
        return "\n".join(
            "This program is provided under the terms of the GNU Affero GPL v3",
            "Source code is available at https://github.com/VICSES/do-forwarder/tree/master",
        )

    # TODO: Only transfer to permitted numbers


    def _cmd_(self, args, from_num, to_num, body, time):
        # :
        # Acknowledge a scheduled transfer
        raise NotImplementedError("schedule")


    def _cmd_transfer(self, args, from_num, to_num, body, time):
        # :transfer <phone number>
        # :transfer <name>
        # :transfer
        #
        # Any alpha characters mean the parameter is a <name>
        # If no parameter is supplied <name> is the sender
        # The target number must be known and approved
        # The source number must be known and approved
        # Notify: Current and new redirect

        if re.search('[a-zA-Z]', args):
            # Any alpha characters -> name
            # Lookup will raise an exception if the name was not found
            args = self._lookup_phonebook(args)

        # No alpha characters -> number
        num = re.sub(r"\D", "", args)

        # handle :transfer case
        if len(num) == 0:
            num = from_num

        # Must be a sane Australian mobile number
        # Can be either local or international format
        # Must output international format
        if num.startswith("04") and len(num) == 10:
            num = '61' + num[1:]

        if not num.startswith('614') or len(num) != 11:
            raise CommandParser.Error("{} is badly formatted number".format(num))


        old_num = self._get_redirect()

        self._set_redirect(num)

        if from_num != old_num:
            self._notify(old_num, "DO transferred from you to {}".format(num))
        if from_num != num:
            self._notify(num, "DO transferred to you from {}".format(old_num))


        pretty_old = old_num if from_num != old_num else "you"
        pretty_new = num if from_num != num else "you"
        return "DO transfered from {} to {}".format(pretty_old, pretty_new)

    def _notify(self, num, text):
        raise NotImplementedError("Notify")


    def _get_redirect(self):
        raise NotImplementedError("Get redirect")


    def _cmd_keep(self, args, from_num, to_num, body, time):
        # :keep
        # Keep the current redirect, disables the schedule
        # The schedule will be resumed after the next manual transfer
        # Notify: Current redirect, next scheduled redirect
        raise NotImplementedError("schedule")



    def _cmd_current(self, args, from_num, to_num, body, time):
        # :current
        # Provides details of current redirect and next two scheduled times
        # Notify: None
        raise NotImplementedError("schedule")


    def _lookup_phonebook(self, name):
        # Raise an exception if the name is not found
        raise NotImplementedError("Phonebook lookup")

    def _set_redirect(self, num):
        raise NotImplementedError("Set redirect")
