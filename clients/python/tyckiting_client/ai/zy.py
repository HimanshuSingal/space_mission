import random

from tyckiting_client.ai import base
from tyckiting_client import actions


class Ai(base.BaseAi):
    """
    Dummy bot that moves randomly around the board.
    """
    
    def respond(self, bots, events):
        ret = []
        for e in events:
            if e.event == 'detected' or e.event=='hit' or e.event=='damaged':
                for b in bots:
                    if b.bot_id == e.bot_id:
                        pos = self.far_pos(b)
                        bots.remove(b)
                        ret.append(actions.Move(bot_id=b.bot_id,x=pos.x,y=pos.y))
            elif e.event == 'see':
                b = (b for b in bots if b.bot_id == e.source).next()
                bots.remove(b)
                pos = self.far_pos(b)
                ret.append(actions.Move(bot_id=b.bot_id,x=pos.x,y=pos.y))
                for b in bots:
                    ret.append(actions.Cannon(bot_id=b.bot_id,x=e.pos.x,y=e.pos.y))
                    bots.remove(b)
                return ret
            elif e.event == 'radarEcho':
                b_last = bots[-1]
                bots.remove(b_last)
                ret.append(actions.Radar(bot_id=b_last.bot_id,x=e.pos.x,y=e.pos.y))
                for b in bots:
                    ret.append(actions.Cannon(bot_id=b.bot_id,x=e.pos.x,y=e.pos.y))
                    bots.remove(b)
                return ret
            else:
                 continue

        for b in bots:
            r_pos = random.choice(list(self.get_valid_radars(b)))
            ret.append(actions.Radar(bot_id=b.bot_id,x=r_pos.x,y=r_pos.y))

        return ret



    
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
                bots.remove(bot)
        
        response = self.respond(bots,events)
                                         
        return response
        
    def far_pos(self,bot):
        pos = list(self.get_valid_moves(bot))
        max_pos = -1
        m_dis = -1
        for p in pos:
            if abs(p.x) > 14 or abs(p.y) > 14:
                pos.remove(p)
                continue
            else:
                dis = (p.x - bot.pos.x) **2 + (p.y - bot.pos.y) **2
                if m_dis < dis:
                    m_dis = dis
                    max_pos = pos.index(p)

        return pos[max_pos]
