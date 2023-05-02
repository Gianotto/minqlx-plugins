# minqlx - A Quake Live server administrator bot.
# Copyright (C) 2015 Mino <mino@minomino.org>

# This file is part of minqlx.

# minqlx is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# minqlx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with minqlx. If not, see <http://www.gnu.org/licenses/>.

import minqlx

VERSION = "v1.00"

class roundcontrol(minqlx.Plugin):
    #####
    # Script blocks new players to join the game after ## rounds was won by any team.
    # Allow players to say !unlockteams to let spectators to join.
    # 
    # Server setup:
    # qlx_minRoundsToLock 5         (default:5)      Minimum rounds won to block new players from joinning
    # qlx_roundControlEnable 1      (default: 1)     Enable / disable round control
    # qlx_autoteamsize 0            (default: 0)     Enable / disable auto teamsize adjustments
    #
    #####
    teamslocked = False

    def __init__(self):
        super().__init__()
        self.add_hook("round_start", self.handle_round_start)
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("player_disconnect", self.handle_player_disconnect)
        self.add_hook("team_switch", self.handle_team_switch)
        self.add_hook("vote_ended", self.handle_vote_ended, priority=minqlx.PRI_LOWEST)

        self.add_command(("unlockteams"), self.cmd_unlockteams)
        self.add_command(("lockstatus"), self.cmd_lockstatus)
        self.add_command(("lockteams"), self.cmd_lockteams, 2, usage="<0|1>")

        self.set_cvar_once("qlx_minRoundsToLock", "5")
        self.set_cvar_once("qlx_roundControlEnable", "1")
        self.set_cvar_once("qlx_autoteamsize", "0")

    def handle_round_start(self, *args, **kwargs):
       if self.get_cvar("qlx_roundControlEnable", bool):
            teams = self.teams()
            if len(teams["red"] + teams["blue"]) % 2 != 0: # Check if teams has same amount of players
                self.msg("Teams were ^3NOT^7 balanced. Not possible to lock teams.")
                return minqlx.RET_STOP_ALL
       
            total_rounds = max((int)(self.game.red_score), (int)(self.game.blue_score)) # gets the maximum rounds won by a team
            if total_rounds >= (int)(self.get_cvar("qlx_minRoundsToLock")) and self.teamslocked is False:
                self.msg("Round Control: Game reach maximum round count. ^6Locking teams.")
                self.msg("Round Control: You can use ^3!unlockteams ^7to unlock.")
                
                self.def_lock()
            if self.teamslocked: self.msg("Round Control: Teams ^1LOCKED^7. Use ^3unlockteams ^7to unlock.")
       
    def handle_player_disconnect(self, player, reason):
        teams = self.teams()
        if len(teams["red"] + teams["blue"]) % 2 != 0: # check if disconnected player was in a team
            self.def_unlock(0)
    
    def handle_team_switch(self, player, old_team, new_team):
        if new_team == "spectator": # check if leaver was in the red or blue team
            self.def_unlock(0)
    
    def handle_game_end(self, data):
        if self.get_cvar("qlx_roundControlEnable", bool):
            self.def_unlock((int)(self.game.teamsize) + 1)
    
    def handle_vote_ended(self, votes, vote, args, passed):
        if vote.lower() == "teamsize" and passed:
            if self.get_cvar("qlx_roundControlEnable", bool):
                self.def_unlock(0)
    
    def cmd_unlockteams(self, player, msg, channel):
        if self.get_cvar("qlx_roundControlEnable", bool):
            if self.teamslocked:
                self.def_unlock((int)(self.game.teamsize) + 1)
            else:
                self.msg("Teams are already ^3UNLOCKED^7.")
        else:
            self.msg("Round Control: Team locking is disabled. Check server configuration.")
        
    def cmd_lockteams(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        if (msg[1] == "1"):
            self.def_lock()
        else:
            self.def_unlock((int)(self.game.teamsize) + 1)

    @minqlx.thread
    def def_unlock(self, size):
        self.unlock()
        self.teamslocked = False
        if size > 0:
            if self.get_cvar("qlx_autoteamsize", bool):
                self.game.teamsize = size
                self.msg("Round Control: Teamsize set to ^3{}.".format(size))
        self.msg("Round Control: Teams were ^3UNLOCKED^7. Spectators are allowed to join.")
    
    @minqlx.thread
    def def_lock(self):
        teams = self.teams()
        self.lock()
        self.teamslocked = True
        if self.get_cvar("qlx_autoteamsize", bool):
            self.game.teamsize = len(teams["red"]) # teams are equal anyways ;)
            self.msg("Round Control: Teamsize set to ^3{}.".format(len(teams["red"])))
        self.msg("Round Control: Teams were ^1LOCKED^7.")
    
    def cmd_lockstatus(self, player, msg, channel):
        if self.get_cvar("qlx_roundControlEnable", bool):
            if self.teamslocked:
                player.tell("Round Control: Teams are ^1LOCKED^7.")
            else:
                player.tell("Round Control: Teams are ^3UNLOCKED^7.")
        else:
            self.msg("Round Control: Team locking is disabled. Check server configuration.")
