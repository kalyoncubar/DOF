from models.vote import Vote
from models.rc import RC


RC_THRESHOLD = 5


class VoteService:

    def __init__(
        self,
        vote_repo,
        comment_repo,
        rc_repo
    ):
        self.vote_repo = vote_repo
        self.comment_repo = comment_repo
        self.rc_repo = rc_repo

    # -------------------------
    # Public API
    # -------------------------
    def cast_vote(
        self,
        comment_id: int,
        user_id: int,
        vote_type: str
    ):
        """
        Like / Dislike ekler veya günceller
        """
        comment = self.comment_repo.get_by_id(comment_id)
        if not comment:
            raise ValueError("Comment not found")

        existing_vote = self.vote_repo.get_by_comment_and_user(
            comment_id, user_id
        )

        if existing_vote:
            existing_vote.vote_type = vote_type
        else:
            self.vote_repo.add(Vote(
                id=0,
                comment_id=comment_id,
                user_id=user_id,
                vote_type=vote_type
            ))

        self._evaluate_comment_for_rc(comment_id)

    # -------------------------
    # Internal logic
    # -------------------------
    def _evaluate_comment_for_rc(self, comment_id: int):
        votes = self.vote_repo.list_by_comment(comment_id)

        like_count = sum(1 for v in votes if v.is_like())
        dislike_count = sum(1 for v in votes if v.is_dislike())

        score = like_count - dislike_count

        existing_rc = self.rc_repo.get_by_source_comment(comment_id)

        if score >= RC_THRESHOLD:
            if not existing_rc:
                self._create_rc_from_comment(comment_id)
            elif existing_rc.is_closed():
                existing_rc.reopen()
        else:
            if existing_rc and existing_rc.is_open():
                existing_rc.close()

    def _create_rc_from_comment(self, comment_id: int):
        comment = self.comment_repo.get_by_id(comment_id)

        rc = RC(
            id=0,
            nc_id=comment.nc_id,
            title="Auto RC from comment",
            description=comment.content,
            created_by_user_id=comment.created_by_user_id,
            source=RC.SOURCE_COMMENT,
            source_comment_id=comment.id
        )

        self.rc_repo.add(rc)
