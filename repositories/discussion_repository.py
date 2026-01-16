# repositories/discussion_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.discussion_comment import DiscussionComment
from models.discussion_vote import DiscussionVote

class DiscussionRepository:
    def __init__(self, s: Session): self.s = s

    def add_comment(self, nc_id: int, user_id: int, text: str, parent_id=None) -> int:
        c = DiscussionComment(nc_id=nc_id, user_id=user_id, text=text, parent_id=parent_id)
        self.s.add(c); self.s.flush(); return c.id

    def add_vote(self, comment_id: int, user_id: int, delta: int) -> int:
        v = self.s.query(DiscussionVote).filter_by(comment_id=comment_id, user_id=user_id).first()
        if v: v.delta = delta
        else: self.s.add(DiscussionVote(comment_id=comment_id, user_id=user_id, delta=delta))
        self.s.flush()
        return self.score_of(comment_id)

    def score_of(self, comment_id: int) -> int:
        return self.s.query(func.coalesce(func.sum(DiscussionVote.delta), 0))\
                     .filter(DiscussionVote.comment_id==comment_id).scalar()
