from flask import Blueprint, abort, make_response, request, Response
from sqlalchemy import desc
from app.models.goal import Goal
from .route_utilities import validate_task, validate_post_attribute, validate_goal
import os
from slack_sdk import WebClient
from ..db import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_task():
    request_body = request.get_json()
    
    title = validate_post_attribute(request_body, "title")

    new_goal = Goal(title=title)
    db.session.add(new_goal)
    db.session.commit()

    response = new_goal.to_dict()

    return response, 201

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

@goals_bp.put("/<goal_id>")
def update_one_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goals_bp.delete("/<goal_id>")
def delete_goal_with_id(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")