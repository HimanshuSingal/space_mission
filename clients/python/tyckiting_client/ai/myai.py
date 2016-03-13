import random

from tyckiting_client.ai import base
from tyckiting_client import actions

class Ai(base.BaseAi):

    a = 0
    wait_list = []

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

        if len(Ai.wait_list) != 0:
            for wait in Ai.wait_list:
                b_id = wait[0];pos = wait[-1]
                b = (b for b in bots if b_id == b.bot_id).next()
                bots.remove(b) # remove the intereted bot from event,bot,wait_list
                Ai.wait_list.remove(wait)
                for e in events:
                    if e.source == b_id or e.bot_id==b_id:
                        events.remove(e)
                response.append(actions.Cannon(bot_id=b_id,x=pos.x,y=pos.y))

        for e in events:
            if e.event == 'see':
                b = (b for b in bots if e.source == b.bot_id).next()
                if b != None:
                    bots.remove(b)
                    response.append(self.on_see(e,b))
                else:
                    print "I am none"

        for bot in bots:
            if not bot.alive:
                continue

            move_pos = random.choice(list(self.get_valid_moves(bot)))
            response.append(actions.Move(bot_id=bot.bot_id,
                                         x=move_pos.x,
                                         y=move_pos.y))
        return response

    def get_far_pos(self,bot,tar_pos):
        dis = []
        pos_list = list(self.get_valid_moves(bot))
        for pos in pos_list:
            d = (pos.x - tar_pos.x)**2 + (pos.y - tar_pos.y)**2
            dis.append(d)

        pos = pos_list[dis.index(max(dis))]
        return pos

    #todo

    def on_see(self,event,bot):
        en_pos = event.pos
        far_pos = self.get_far_pos(bot,en_pos) # get the farest pos, move
            # and shoot next turn
        Ai.wait_list.append([bot.bot_id,'cannon',en_pos])
        print(Ai.wait_list)
        return actions.Move(bot_id=bot.bot_id,x=far_pos.x,y=far_pos.y)

    def on_radar_echo(self):
        return

    def on_detected(self):
        return

    def on_hit(self):
        return

    def give_priority(self,events,bots):
       pass