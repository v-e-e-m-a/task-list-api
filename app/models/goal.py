from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)

    def to_dict(self):
        """Return a plain dict of this Task's attribute values.

        `to_dict` is an instance method (not a classmethod) so it returns
        the values stored on the instance, not SQLAlchemy mapped-column
        objects. `completed_at` is returned as an ISO-formatted string when
        present, otherwise None.
        """
        goal_as_dict = {
            "id": self.id,
            "title": self.title
        }

        return goal_as_dict

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(title=goal_data["title"])

        return new_goal
