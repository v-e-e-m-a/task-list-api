from flask import Blueprint, abort, make_response, request, Response
from sqlalchemy import desc
from app.models.goal import Goal
from .route_utilities import validate_task, validate_post_attribute, validate_goal
import os
from slack_sdk import WebClient
from ..db import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.get("/<goal_id>")
def get_goal_by_id(goal_id):
    goal = validate_goal(goal_id)

    return goal.to_dict()

@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)

    goals = db.session.scalars(query)

    goals_response = []

    for goal in goals:
        goals_response.append(goal.to_dict())

    return goals_response