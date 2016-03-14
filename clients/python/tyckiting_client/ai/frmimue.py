import random

from tyckiting_client.ai import base
from tyckiting_client import actions


class Ai(base.BaseAi):
    """
    Dummy bot that moves randomly around the board.
    """
    
    def respond(self, bot, events):
            
        for e in events:
            if e.event == "see" and e.source == bot.bot_id:
                valid_moves = list(self.get_valid_moves(bot))
                far_moves = []
                for vm in valid_moves:
                    if abs(vm.x - bot.pos.x) > 1 or abs(vm.y - bot.pos.y) > 1:
                        far_moves.append(vm);
                move_pos = random.choice(far_moves);
                return actions.Move(bot_id=bot.bot_id,
                                        x=move_pos.x,
                                        y=move_pos.y)
            if e.event == "see" and e.source != bot.bot_id:
                cannon_pos = e.pos;
                return actions.Cannon(bot_id=bot.bot_id,
                                x=cannon_pos.x,
                                y=cannon_pos.y)
                                
        valid_moves = list(self.get_valid_moves(bot))
        far_moves = []
        for vm in valid_moves:
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
        
        for bot in bots:
            if not bot.alive:
                continue
            response.append(self.respond(bot, events))
                        
                                         
        return response
        
