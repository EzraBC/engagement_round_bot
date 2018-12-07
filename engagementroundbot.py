import telegram.ext as tele
import configparser
import datetime
import json

class UsernameFilter(tele.BaseFilter):
    def filter(self, message):
        return message.text.startswith('@')

username_filter = UsernameFilter()

class EngagementRoundBot:

    def __init__(self, config_file, persistence=None):
        config = configparser.ConfigParser()
        config.read(config_file)
        self._token = config['BOT_INFO']['token']
        self._round_info = dict(config['ROUND_INFO'])
        self.updater = tele.Updater(token=self._token)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue
        self.make_commands()

    def opt_in(self, bot, update):
        # Add at beginning of window, remove at end
        user = update.message.from_user
        rec_give = update.message.text.split(', ')
        accs = {
            'user': user,
            'receive': rec_give[0],
            'give': rec_give[-1]
        }
        self.round_users[user.id] = accs
        name = user.first_name if user.username is None else user.username
        msg = (f'{name} has opted in!\n'
               f'Receiving likes on {accs["receive"]},\n'
               f'Giving likes with {accs["give"]}.')
        bot.send_message(chat_id=update.message.chat_id, text=msg)

    def round_info(self, bot, update):
        users = '\n'.join(u['user'].username for u in self.round_users.values())
        msg = 'Users in this round:\n' + users
        bot.send_message(chat_id=update.message.chat_id, text=msg)

    def make_commands(self):
        opt_in_handler = tele.MessageHandler(username_filter, self.opt_in)
        self.dispatcher.add_handler(opt_in_handler)

        round_info_handler = tele.CommandHandler('round_info', self.round_info)
        self.dispatcher.add_handler(round_info_handler)

    def start_round(self):
        self.allow_optins()

    def read_config(self, config):
        pass

    def start(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()

    def schedule_rounds(self, bot, job):
        self._rounds

    def intiate_daily_job(self):
        self.job_queue.run_daily(self.schedule_rounds, datetime.time(22))

class Round:

    def __init__(self, start_time, join_window, engage_window):
        self.start_time = datetime.time(start_time)
        self.join_window = self._tdstr(join_window)
        self.engage_window = self._tdstr(engage_window)
        self._started = False
        self._users = {}
        self._receivers = set()

    def _tdstr(self, s):
        val_types = ('hours', 'minutes', 'seconds')
        num = float(s[:-1])
        k = next(x for x in val_types if x.startswith(s[-1]))
        return datetime.timedelta(**{k: num})

    def add(self, user, receive, give=None):
        if receive in self._receivers and user.id not in self._users:
            return
        self._receivers.add(receiver)
        self._users[user.id] = {
            'user': user,
            'receive': receive,
            'give': receive if give is None else give
        }

    @classmethod
    def make_rounds(cls, start_times, join_window, engage_window):
        start_times = map(int, start_times.split(','))
        return [cls(st, join_window, engage_window) for st in start_times]
        

# ROUND
'''
start round:
    accept opt-ins and save users
    2-minute warning
    send dms to users with all receive handles except own

    check if engaged at 20

    check if engaged at 40

    check if engaged at 2 min warning

    distribute strikes
'''
