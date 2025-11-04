from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, DateTime, ForeignKey
from typing import Optional, TYPE_CHECKING
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    is_complete: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, server_default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship("Goal", back_populates="tasks")
    
    def to_dict(self):
        task_as_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete if self.is_complete else False
        }

        if self.goal:
            task_as_dict["goal_id"] = self.goal.id

        return task_as_dict
    
    @classmethod
    def from_dict(cls, task_data):
        # Required fields
        title = task_data["title"]
        description = task_data["description"]

        # Optional fields with sensible defaults
        is_complete = task_data.get("is_complete", False)
        completed_at = task_data.get("completed_at", None)

        new_task = cls(
            title=title,
            description=description,
            is_complete=is_complete,
            completed_at=completed_at,
        )

        return new_task