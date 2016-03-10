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
        response = []
        b_id = []

        for e in events:
            if e.event == 'see':
                # print e.pos["x"],'\t',e.pos["y"]
                b = (b for b in bots if b["bot_id"]==e.source)
                idx = (idx for idx,b in bots if b["bot_id"]==e.source)
                bots.pop(idx)
                # c_pos = list(self.get_valid_cannons(b))
                # print c_pos
                response.append(actions.Cannon(bot_id=b.bot_id,x=e.pos.x,y=e.pos.y))
            elif e.event == 'radarEcho':
                print '\t\t\t\t\techo',e.pos.x,'\t',e.pos.y
                b = bots.pop(-1)
                c_pos = list(self.get_valid_cannons(b))
                print c_pos
                response.append(actions.Cannon(bot_id=b.bot_id,x=e.pos.x,y=e.pos.x))
            else:
                for b in bots:
                    move_pos = random.choice(list(self.get_valid_moves(b)))
                    radar_pos = random.choice(list(self.get_valid_radars(b)))
                    m = actions.Move(bot_id=b.bot_id,x=move_pos.x,y=move_pos.y)
                    r = actions.Radar(bot_id=b.bot_id,x=radar_pos.x,y=radar_pos.y)
                    act = r if Ai.a % 3 == 0 else m
                    response.append(act)

        Ai.a = Ai.a + 1
        return response
