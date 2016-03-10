import random

from tyckiting_client.ai import base
from tyckiting_client import actions

class Ai(base.BaseAi):

    a = 0

    def move(self, bots, events):
        """
        Move the bot to a random legal positon.

        Args:
            bots: List of bot states for own team
            events: List of events form previous round

        Returns:
            List of actions to perform this round.
        """
        b_id = []
        response = []

        for e in events:
            if e.event == 'see':
                b = (b for b in bots if b.bot_id==e.source).next()
                print '\t\t\t\t\tsee'
                b_id.append(b.bot_id)
                pos = self.get_far_pos(b,e.pos)
                response.append(actions.Cannon(bot_id=b.bot_id,x=pos.x,y=pos.y))
                # print '\t\t\tsee\t',e.pos.x,',',e.pos.y
            elif e.event == 'radarEcho':    
                b = bots[events.index(e)]
                b_id.append(b.bot_id)
                response.append(actions.Cannon(bot_id=b.bot_id,x=e.pos.x,y=e.pos.x))
                # print '\t\t\techo\t',e.pos.x,',',e.pos.y
            else:
                for b in bots:
                    if b.bot_id not in b_id:
                        move_pos = random.choice(list(self.get_valid_moves(b)))
                        radar_pos = random.choice(list(self.get_valid_radars(b)))
                        m = actions.Move(bot_id=b.bot_id,x=move_pos.x,y=move_pos.y)
                        r = actions.Radar(bot_id=b.bot_id,x=radar_pos.x,y=radar_pos.y)
                        act = m if Ai.a % 3 == 0 else r
                        response.append(act)
                        b_id.append(b.bot_id)
                    else:
                        continue

        Ai.a = Ai.a + 1
        return response

    def get_far_pos(self,bot,tar_pos):
        dis = []
        pos_list = list(self.get_valid_moves(bot))
        for pos in pos_list:
            d = (pos.x - tar_pos.x)**2 + (pos.y - tar_pos.y)**2
            dis.append(d)

        pos = pos_list[dis.index(max(dis))]
        return pos