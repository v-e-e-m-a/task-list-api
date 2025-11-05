from flask import Blueprint, abort, make_response, request, Response
from sqlalchemy import desc
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_post_attribute, validate_model, create_model
import os
from ..db import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()
    
    title = validate_post_attribute(request_body, "title")

    goal_data = {
        "title": title
    }

    new_goal = create_model(Goal, goal_data)

    return new_goal

@goals_bp.get("/<goal_id>")
def get_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)

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
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goals_bp.delete("/<goal_id>")
def delete_goal_with_id(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goals_bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()

    validate_post_attribute(request_body, "task_ids")

    task_ids = request_body["task_ids"]

    tasks_to_add = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        tasks_to_add.append(task)

    goal.tasks = tasks_to_add

    db.session.commit()

    response = {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks]
    }

    return response

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks = [task.to_dict() for task in goal.tasks]
    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks
    }
    return response

