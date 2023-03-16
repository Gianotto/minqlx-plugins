#####
# The Telegram BOT
# Relay ingame chat to the chatbot in Telegram
# Requires: 
#   pyTelegramBOTAPI (https://pypi.org/project/pyTelegramBotAPI/)
#   Add the module into the minqlx.zip file on the server on the
#   path ~/steamapps/common/qlds
#   
#   Create a new bot using the Bot Father.
#   Define API_KEY using command !telebotapikey <KEY>
#   Use Telegram app to call command /chatid. Bot will reply with the ID.
#   Define CHAT_ID using command !telebotchatid <ID>
#
#   API_KEY is the key token for your bot.
#   CHAT_ID is the chat id used in Telegram app.
#   
#####
import minqlx
from telebot import TeleBot, util

VERSION = "v0.1"
TELEBOT_DB_KEY = "minqlx:telegrambot:{}"
API_KEY = "6074681084:AAFgdc3hPThmameomSsujwyJOt2Pck0Z_JQ"
telebot = TeleBot(API_KEY)

class telegrambot(minqlx.Plugin):
    gamebot = telebot
    complete = False # setup complete control flag
    apikeyk = ""
    chatidk = ""

    def __init__(self):
        super().__init__()
        self.add_hook("chat", self.handle_chat)
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("player_connect", self.handle_player_connect, priority=minqlx.PRI_LOWEST)
        self.add_hook("player_disconnect", self.handle_player_disconnect)
        self.add_hook("vote_called", self.handle_vote_called)
        self.add_hook("vote_ended", self.handle_vote_ended)
        self.add_hook("map", self.handle_map)
        self.add_hook("unload", self.handle_unload)

        self.add_command("testpl", self.testpl, 2)
        self.add_command("telebotchatid", self.chatid, 2, usage="<CHAT_ID>")
        self.add_command("telebotapikey", self.apikey, 2, usage="<API_KEY>")
        self.add_command("showtelebotkeys", self.telebotkey, 2)
        
        minqlx.console_print("Loading Telegram Bot keys from DB...")
        self.loadkeys()

    @gamebot.message_handler(commands=['chatid'])
    def cmd_chatid(message):
        telebot.send_message(message.chat.id, "Chat ID: {}".format(message.chat.id))
    
    @gamebot.message_handler(commands=['time'])
    def cmd_time(message):
        minqlx.console_command("!time")
    
    @gamebot.message_handler(commands=['unlockteams'])
    def cmd_teams(message):
        minqlx.console_command("!unlockteams")

    @gamebot.message_handler(commands=['map'])
    def cmd_map(message):
        map = util.extract_arguments(message.text)
        minqlx.Plugin.change_map("{}".format(map), "ca")

    @gamebot.message_handler(commands=['say'])
    def cmd_say(message):
        text = util.extract_arguments(message.text)
        telebot.send_message(message.chat.id, "Telebot: {}".format(text)) # feedback
        minqlx.CHAT_CHANNEL.reply("Telebot: {}".format(text))
    
    ###################### DB ######################
    @minqlx.thread
    def loadkeys(self):
        # Get API KEY in DB
        apikey = self.db.get(TELEBOT_DB_KEY.format("apikey"))
        if apikey == "":
            minqlx.console_print("Telegram Bot: No API KEY defined. Telegram Bot will not work.")
            minqlx.console_print("Telegram Bot: Setup using !telebotapikey <API_KEY> from the Bot configuration.")
            return minqlx.RET_STOP_ALL
        else:
            minqlx.console_print("Telegram Bot: API KEY found: {}".format(apikey))
            self.apikeyk = apikey
            #self.gamebot.setapikey(apikey)

        # Get CHAT ID in DB
        chatidkey = self.db.get(TELEBOT_DB_KEY.format("chatid"))
        if chatidkey == "":
            self.msg("Telegram Bot: No Chat ID defined. Telegram Bot will not send any message.")
            self.msg("Telegram Bot: Setup using !telebotchatid <CHAT_ID> from the telegram /chatid comamnd.")
            return minqlx.RET_STOP_ALL
        else:
            minqlx.console_print("Telegram Bot: CHAT ID found: {}".format(chatidkey))
            self.chatidk = chatidkey
        
        if self.apikeyk != "" and self.chatidk != "":
            self.complete = True
            self.gamebot.polling()

    ###################### DB SET ######################
    def chatid(self, player, msg, channel):
        if len(msg) < 1:
            return minqlx.RET_USAGE
        else:
            self.db.set(TELEBOT_DB_KEY.format("chatid"), msg[1])
            player.tell("Telegram Bot: Chat ID updated.")

    def apikey(self, player, msg, channel):
        if len(msg) < 1:
            return minqlx.RET_USAGE
        else:
            self.db.set(TELEBOT_DB_KEY.format("apikey"), msg[1])
            player.tell("Telegram Bot: API KEY updated.")

    def telebotkey(self, player, msg, channel):
        player.tell("Telegram Bot: API KEY: {}".format(self.db.get(TELEBOT_DB_KEY.format("apikey"))))
        player.tell("Telegram Bot: CHAT ID: {}".format(self.db.get(TELEBOT_DB_KEY.format("chatid"))))

    ################### HANDLES ####################
    ###################  UNLOAD  ####################    
    def handle_unload(self, plugin):
        if plugin == self.__class__.__name__:
            self.gamebot.stop_polling()

    ###################  VOTES  ####################
    def handle_vote_called(self, caller, vote, args):
        if self.complete: self.scan_vote_called(caller, vote, args)
    
    @minqlx.thread
    def scan_vote_called(self, caller, vote, args):
        c = self.clean_text((str)(caller))
        self.gamebot.send_message(self.chatidk, "{}: callvote {} {}".format(c, vote, args))
    
    def handle_vote_ended(self, votes, vote, args, passed):
        if passed:
            self.gamebot.send_message(self.chatidk, "Vote passed ({} - {}).".format(*votes))
        else:
            self.gamebot.send_message(self.chatidk, "{}: Vote failed.".format(vote))

    ###################   CHAT   ####################
    def handle_chat(self, player, msg, channel):
        if self.complete: self.scan_chat(player, msg, channel)
    
    @minqlx.thread
    def scan_chat(self, player, msg, channel):
        if channel == "chat":
            p = self.clean_text((str)(player))
            self.gamebot.send_message(self.chatidk, "{}: {}".format(p, msg))

    ################### PLAYER ####################
    def handle_player_connect(self, player):
        if self.complete: self.scan_player_connect(player)
    
    @minqlx.thread
    def scan_player_connect(self, player):
        p = self.clean_text((str)(player))
        self.gamebot.send_message(self.chatidk, "{} connected.".format(p))

    def handle_player_disconnect(self, player, reason):
        if self.complete: self.scan_player_disconnect(player)
    
    @minqlx.thread
    def scan_player_disconnect(self, player):
        p = self.clean_text((str)(player))
        self.gamebot.send_message(self.chatidk, "{} disconnected.".format(p))

    ###################  MAP  ####################
    def handle_map(self, map, factory):
        if self.complete: self.scan_map(map, factory)

    @minqlx.thread
    def scan_map(self, map, factory):
        self.gamebot.send_message(self.chatidk, "Changing to map {}.".format(map))
    
    ################### GAME END ####################
    def handle_game_end(self, data):
        if self.complete: self.scan_game_end(data)

    @minqlx.thread
    def scan_game_end(self, data):
        if self.complete:
            players = self.players()
            if not len(players):
                return minqlx.RET_STOP_ALL
            
            res = "{:^}\n"
            teamr = res.format("-- Red --")
            teamb = res.format("-- Blue --")
            spec = res.format("-- Spec --")
            for p in players:
                if p.team == 'red':
                    teamr += "{}\n".format(self.clean_text((str)(p)))
                if p.team == 'blue':
                    teamb += "{}\n".format(self.clean_text((str)(p)))
                if p.team == 'spectator':
                    spec += "{}\n".format(self.clean_text((str)(p)))
            
            self.gamebot.send_message(self.chatidk, teamr)
            self.gamebot.send_message(self.chatidk, teamb)
            self.gamebot.send_message(self.chatidk, spec)

    @minqlx.thread
    def testpl(self, player, msg, channel):
        if self.complete:
            players = self.players()
            if not len(players):
                player.tell("There are no players connected at the moment.")
                return minqlx.RET_STOP_ALL
            
            res = "{:^}\n"
            teamr = res.format("-- Red --")
            teamb = res.format("-- Blue --")
            spec = res.format("-- Spec --")
            for p in players:
                if p.team == 'red':
                    teamr += "{}\n".format(self.clean_text((str)(p)))
                if p.team == 'blue':
                    teamb += "{}\n".format(self.clean_text((str)(p)))
                if p.team == 'spectator':
                    spec += "{}\n".format(self.clean_text((str)(p)))
            
            self.gamebot.send_message(self.chatidk, teamr)
            self.gamebot.send_message(self.chatidk, teamb)
            self.gamebot.send_message(self.chatidk, spec)