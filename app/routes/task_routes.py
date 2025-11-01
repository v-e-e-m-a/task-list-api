from flask import Blueprint, abort, make_response, request
from app.models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    id = request_body["id"]
    title = request_body["title"]
    description = request_body["description"]
    is_complete = request_body["is_complete"]
    # completed_at = request_body["completed_at"]

    new_task = Task(id=id, title=title, description=description, is_complete=is_complete)
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

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"message": f"task {task_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    
    if not task:
        response = {"message": f"task {task_id} not found"}
        abort(make_response(response, 404))

    return task


