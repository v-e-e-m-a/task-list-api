from flask import abort, make_response
from app.models.task import Task
from ..db import db

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

def validate_post_attribute(request_body, attribute):
    if request_body.get(attribute):
        return request_body[attribute]
    else:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))