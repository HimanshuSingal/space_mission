import random

from tyckiting_client.ai import base
from tyckiting_client import actions

class Ai(base.BaseAi):
    """
    Dummy bot that moves randomly around the board.
    """
    
    shoot_target = [[[-1, 1], [1, -1]], [[0, 1], [0, -1]]]
    
    def respond(self, bot, events):
            
        for e in events:
            if e.event == "radarEcho" or e.event == "see":
                shooting = random.choice(self.shoot_target)
                if self.botnumber == 0:
                    radar_pos = e.pos
                    return actions.Radar(bot_id=bot.bot_id,
                                    x=radar_pos.x,
                                    y=radar_pos.y)
                elif self.botnumber == 1:
                    cannon_pos = e.pos;
                    return actions.Cannon(bot_id=bot.bot_id,
                                    x=cannon_pos.x + shooting[0][0],
                                    y=cannon_pos.y + shooting[0][1])
                elif self.botnumber == 2:
                    cannon_pos = e.pos;
                    return actions.Cannon(bot_id=bot.bot_id,
                                    x=cannon_pos.x + shooting[1][0],
                                    y=cannon_pos.y + shooting[1][1])
                                
        radar_pos = random.choice(list(self.get_valid_radars(bot)));
        return actions.Radar(bot_id=bot.bot_id,
                                 x=radar_pos.x,
                                 y=radar_pos.y)
                                 
    def random_move(self, bot, events):
        valid_moves = list(self.get_valid_moves(bot))
        far_moves = []
        for vm in valid_moves:
            if vm.x < -14 or vm.x > 14 or vm.y < -14 or vm.y > 14:
                continue
            if abs(vm.x - bot.pos.x) > 1 or abs(vm.y - bot.pos.y) > 1:
                far_moves.append(vm);
        move_pos = random.choice(far_moves);
        return actions.Move(bot_id=bot.bot_id,
                                    x=move_pos.x,
                                    y=move_pos.y)
    
    def move(self, bots, events):
        """
        Move the bot to a random legal positon.

        Args:
            bots: List of bot states for own team
            events: List of events form previous round

        Returns:
            List of actions to perform this round.
        """
        
        
        
        response = []
        self.botnumber = 0
        currentBots = []
        
        for e in events:
            if e.event == "detected":
                for b in bots:
                    if e.bot_id == b.bot_id:
                        response.append(self.random_move(b, events));
                        bots.remove(b)
            if e.event == "see":
                for b in bots:
                    if e.source == b.bot_id:
                        response.append(self.random_move(b, events));
                        bots.remove(b)
        
        if len(bots) == 1:
            self.botnumber = 1
        
        for bot in bots:
            if not bot.alive:
                continue    
                
            response.append(self.respond(bot, events))
            
            self.botnumber += 1
                                       
        return response
        
