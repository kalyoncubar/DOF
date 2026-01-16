from datetime import datetime
from typing import Optional


class Comment:
    """
    NC altındaki yorumlar (sosyal tartışma alanı)
    """

    def __init__(
        self,
        id: int,
        nc_id: int,
        content: str,
        created_by_user_id: int,
        parent_comment_id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.nc_id = nc_id

        self.content = content
        self.created_by_user_id = created_by_user_id

        # Reply desteği (yorumun cevabı)
        self.parent_comment_id = parent_comment_id

        self.created_at = created_at or datetime.utcnow()

    def is_reply(self) -> bool:
        return self.parent_comment_id is not None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nc_id": self.nc_id,
            "content": self.content,
            "created_by_user_id": self.created_by_user_id,
            "parent_comment_id": self.parent_comment_id,
            "created_at": self.created_at.isoformat()
        }
