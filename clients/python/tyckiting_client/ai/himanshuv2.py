import random

from tyckiting_client.ai import base
from tyckiting_client import actions

class Ai(base.BaseAi):
    """
    Dummy bot that moves randomly around the board.
    """
    
    def respond(self, bot, events):
        print self.botnumber
            
        for e in events:
            if e.event == "radarEcho":
                if self.botnumber == 1:
                    radar_pos = e.pos;
                    return actions.Radar(bot_id=bot.bot_id,
                                    x=radar_pos.x,
                                    y=radar_pos.y)
                elif self.botnumber == 0:
                    cannon_pos = e.pos;
                    return actions.Cannon(bot_id=bot.bot_id,
                                    x=cannon_pos.x-1,
                                    y=cannon_pos.y+1)
                elif self.botnumber == 2:
                    cannon_pos = e.pos;
                    return actions.Cannon(bot_id=bot.bot_id,
                                    x=cannon_pos.x+1,
                                    y=cannon_pos.y-1)
                                
            if e.event == "detected":
                valid_moves = list(self.get_valid_moves(bot))
                far_moves = []
                for vm in valid_moves:
                    if abs(vm.x - bot.pos.x) > 1 or abs(vm.y - bot.pos.y) > 1:
                        far_moves.append(vm);
                move_pos = random.choice(far_moves);
                return actions.Move(bot_id=bot.bot_id,
                                            x=move_pos.x,
                                            y=move_pos.y)
                                
        radar_pos = random.choice(list(self.get_valid_radars(bot)));
        return actions.Radar(bot_id=bot.bot_id,
                                 x=radar_pos.x,
                                 y=radar_pos.y)
    
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
        
        for bot in bots:
            if not bot.alive:
                continue           
                
            response.append(self.respond(bot, events))
            
            self.botnumber += 1
                                       
        return response
        
