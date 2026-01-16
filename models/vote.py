from datetime import datetime


class Vote:
    """
    Like / Dislike
    """

    TYPE_LIKE = "like"
    TYPE_DISLIKE = "dislike"

    def __init__(
        self,
        id: int,
        comment_id: int,
        user_id: int,
        vote_type: str,
        created_at: datetime | None = None
    ):
        if vote_type not in (self.TYPE_LIKE, self.TYPE_DISLIKE):
            raise ValueError("Invalid vote type")

        self.id = id
        self.comment_id = comment_id
        self.user_id = user_id
        self.vote_type = vote_type
        self.created_at = created_at or datetime.utcnow()

    def is_like(self) -> bool:
        return self.vote_type == self.TYPE_LIKE

    def is_dislike(self) -> bool:
        return self.vote_type == self.TYPE_DISLIKE

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "comment_id": self.comment_id,
            "user_id": self.user_id,
            "vote_type": self.vote_type,
            "created_at": self.created_at.isoformat()
        }
