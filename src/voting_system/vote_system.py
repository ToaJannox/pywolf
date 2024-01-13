
from typing import List, Dict,TypedDict

from player_role.player import Player


class Vote(TypedDict):
    votes_against: Player
    has_voted: bool

class VoteSystem:
    def __init__(self) -> None:
        self.votes: Dict[str,Vote] = dict()

    def setup(self, players: List[Player]) -> None:
        for p in players:
            v: Vote = {f"{p.name}" : {"votes_against":None,"has_voted":True}}
            self.votes[p.name] = v

    def reset_votes(self) -> None:
        for vote in self.votes.values():
            vote["has_voted"] = False
            vote["votes_against"] = None

    def remove_voter(self, player: Player) -> None:
        if player.name in self.votes:
            del self.votes[player.name]

    def vote(self, selected_voters: List[Player], with_mayor=False) -> Player:
        result = None
        self._vote_process(selected_voters)
        return result
    
    def faction_vote(self, selected_voters: List[Player]) -> Player:
        return self._vote_process(selected_voters)

    def _vote_process(self, selected_voters: List[Player]) -> None:
        self.reset_votes()
        for voter in selected_voters:
            if voter.name in self.votes:
                targets = selected_voters.copy() # removing self from voting
                targets.remove[voter]
                self.votes[voter.name]["has_voted"] = True
                self.votes[voter.name]["votes_against"] = voter.vote(targets)
        # TODO count vote 
        # TODO make this function generic
        # TODO make this function generic
        # TODO make it used in specialized function to cover specific vote
    
    # def count_votes(self,) -> Dict[str,int]:
    #     result = {name: 0 for name in self.votes.keys()}
    #     for name,vote in self.votes.items():
    #         result[vote["votes_against"]] += 2 if 
    #     return result
    # def get_vote_result(self) -> str:
    #     d = {name: data["votes_against"] for name, data in self.votes.items()} # dict comprehensions
    #     return max(d, key=d.get)
