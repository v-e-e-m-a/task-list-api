from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from .route_utilities import validate_task, validate_post_attribute
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    
    title = validate_post_attribute(request_body, "title")
    description = validate_post_attribute(request_body, "description")
    
    # Use .get so missing 'is_complete' in the request doesn't raise KeyError.
    is_complete = request_body.get("is_complete", False)

    # completed_at = request_body["completed_at"]

    new_task = Task(title=title, description=description, is_complete=is_complete)
    db.session.add(new_task)
    db.session.commit()

    response = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.is_complete,
        # "completed_at": new_task.completed_at
    }

    return response, 201


@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    tasks = db.session.scalars(query.order_by(Task.id))

    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return task.to_dict()

@tasks_bp.put("/<task_id>")
def update_one_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.is_complete = request_body.get("is_complete", False)

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")