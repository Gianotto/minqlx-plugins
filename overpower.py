# Created by sn00per
# Plugin to enable overpower weapon at random or defined by player.
# The overpower will last until next round.

# Plugin CVARS
#   qlx_weaponPower 250
#   qlx_weaponList - comma separated list of weapon codes to enable overpower

# Usage:
#   !overporwer <weapon_code> or <random>
#   !callvote overpower <weapon_code> or <random>

import minqlx
import random

damage_default = {
    "sg": 5,
    "rl": 100,
    "rg": 80,
    "pl": 0,
    "pg": 20,
    "ng": 12,
    "mg": 5,
    "lg": 6,
    "gl": 100,
    "hmg": 8,
    "gh": 10,
    "g": 50,
    "cg": 8,
    "bfg": 100
}

WEAPON_NAME = {
    "sg": "shotgun",
    "rl": "rocket launcher",
    "rg": "railgun",
    "pl": "plumber",
    "pg": "plasma gun",
    "ng": "nailgun",
    "mg": "machine gun",
    "lg": "lightning gun",
    "gl": "granade launcher",
    "hmg": "heavy machine gun",
    "gh": "grappling hook",
    "g": "gauntlet",
    "cg": "chaingun",
    "bfg": "BFG10K"
}

WEAPONS = [
    "hmg",
    "lg",
    "mg",
    "rg"
]

DMG_COMMAND = "g_damage_{}"

class overpower(minqlx.Plugin):
    weapons_changed = []
    callvote_wp = ""
    default_damage = 0

    def __init__(self):
        self.set_cvar_once("qlx_weaponPower", "250")
        self.set_cvar_once("qlx_weaponList", ",".join(WEAPONS))
        self.weapons = self.get_cvar("qlx_weaponList", list)
        self.default_damage = self.get_cvar("qlx_weaponPower", int)
        minqlx.console_print(str(self.default_damage))

        self.add_hook("vote_called", self.handle_vote_called)
        self.add_hook("vote_ended", self.handle_vote_ended)
        self.add_hook("round_end", self.handle_round_end)
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("new_game", self.handle_new_game)

        self.add_command("oplist", self.cmd_oplist)
        self.add_command(("opremove", "oprm"), self.cmd_opremove, 2, usage="<weapon_code>")
        self.add_command(("overpower", "opwp", "op"), self.cmd_overpower, 2, usage="<weapon_code> [damage] or <random>")
        
    def handle_round_end(self, round_number):
        for wp in self.weapons_changed:
            self.removeweapon(wp)
    
    def handle_game_end(self, data):
        for wp in self.weapons_changed:
            self.removeweapon(wp)

    def handle_new_game(self):
        for wp in self.weapons_changed:
            self.removeweapon(wp)

    def handle_vote_called(self, caller, vote, args):
        if vote.lower() == "overpower":
            if len(args) < 1:
                caller.tell("^3Callvote ^7overpower ^3. Try with <weapon_code> or <random>. Allowed weapons: ^7{}".format(", ".join(WEAPONS)))
                return minqlx.RET_STOP_ALL
            if args == "random":
                self.callvote_wp = random.choice(WEAPONS)
                dmg = self.get_cvar("qlx_weaponPower")
                cmd = DMG_COMMAND.format(self.callvote_wp)
                self.callvote("set {} {}".format(cmd, dmg), "^1Overpower ^7weapon ^3{} ^7until next round?".format(WEAPON_NAME[self.callvote_wp]))
                #minqlx.client_command(caller.id, "vote yes")
                self.msg("{}^7 called a vote.".format(caller.name))
            elif args in WEAPONS:
                dmg = self.get_cvar("qlx_weaponPower")
                cmd = DMG_COMMAND.format(args)
                self.callvote("set {} {}".format(cmd, dmg), "^1Overpower ^7weapon ^3{} ^7until next round?".format(WEAPON_NAME[args]))
                #minqlx.client_command(caller.id, "vote yes")
                self.msg("{}^7 called a vote.".format(caller.name))
            return minqlx.RET_STOP_ALL
        
    def handle_vote_ended(self, votes, vote, args, passed):
        if passed and vote.lower() == "overpower":
                if args == "random":
                    self.weapons_changed.append(self.callvote_wp)
                if args not in self.weapons_changed:
                    self.weapons_changed.append(args)

    @minqlx.thread
    def handle_cvar(self, weapon, damage=0, player=None):
        cmd = DMG_COMMAND.format(weapon)
        minqlx.console_print("overpower: set_cvar {} {}".format(cmd, damage))
        self.set_cvar(cmd, damage)
        if player != None:
            player.tell("Weapons ^3{} ^7are ^1overpowered ^7until next round.".format(", ".join(self.weapons_changed)))

    def cmd_overpower(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        try:
            wp = msg[1]
            if wp in WEAPONS: # check if the selected weapon is in the allowed weapon list
                if len(msg) > 2:
                    self.handle_cvar(weapon=wp, damage=int(msg[2]), player=player)
                else:
                    self.handle_cvar(weapon=wp, damage=self.default_damage, player=player)
                if wp not in self.weapons_changed:
                    self.weapons_changed.append(wp)
            elif wp == "random":
                wp = random.choice(WEAPONS)
                self.handle_cvar(weapon=wp, damage=self.default_damage, player=player)
                if wp not in self.weapons_changed:
                    self.weapons_changed.append(wp)
            else:
                player.tell("Weapon ^3{} ^7is not in allowed weapons list.".format(wp))
                        
        except ValueError:
            player.tell("Invalid weapon choice.")
    
    def cmd_opremove(self, player, msg, channel):
        if len(msg) < 1:
            return minqlx.RET_USAGE
        try:
            wp = msg[1]
            if wp in self.weapons_changed:
                self.removeweapon(wp)
                player.tell("Weapon ^3{} ^7damage set to default.".format(wp))
            else:
                player.tell("Weapon ^3{} ^7is not ^1overpowered.".format(wp))

        except ValueError:
            player.tell("Invalid weapon choice.")
    
    def cmd_oplist(self, player, msg, channel):
        if len(self.weapons_changed) > 0:
            player.tell("Weapons ^3{} ^7are ^1overpowered^7.".format(", ".join(self.weapons_changed)))
        else:
            player.tell("No weapons are overpowered.")
            player.tell("Allowed weapons to overpower: ^3{}".format(", ".join(WEAPONS)))

    def removeweapon(self, weapon):
        self.handle_cvar(weapon, damage_default[weapon])
        self.weapons_changed.remove(weapon)