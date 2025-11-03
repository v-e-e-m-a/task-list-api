from flask import Blueprint, abort, make_response, request, Response
from sqlalchemy import desc
from app.models.task import Task, datetime
from .route_utilities import validate_model, validate_post_attribute, create_model
import os
from slack_sdk import WebClient
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    
    title = validate_post_attribute(request_body, "title")
    description = validate_post_attribute(request_body, "description")
    is_complete = request_body.get("is_complete", False)

    task_data = {
        "title": title,
        "description": description,
        "is_complete": is_complete
    }

    new_task = create_model(Task, task_data)

    return new_task


@tasks_bp.get("")
def get_all_tasks():
    sort_param = request.args.get("sort")

    query = db.select(Task)

    if sort_param == "asc":
        query = query.order_by(Task.title)
    
    if sort_param == "desc":
        query = query.order_by(desc(Task.title))

    tasks = db.session.scalars(query)

    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict()

@tasks_bp.put("/<task_id>")
def update_one_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.is_complete = request_body.get("is_complete", False)

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_one_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("<task_id>/mark_complete")
def mark_complete_by_task_id(task_id):
    task = validate_model(Task, task_id)

    task.is_complete = True
    task.completed_at = datetime.now()

    db.session.commit()

    # # Send to Slack API
    # message = f"Someone just completed the task {task.title}"

    # # Set up a WebClient with the Slack OAuth token
    # client = WebClient(token=os.environ.get("SLACK_OAUTH_TOKEN"))

    # # Send a message to Slack
    # client.chat_postMessage(
    #     channel="test-slack-api", 
    #     text=message, 
    #     username="Veema's TaskList API"
    # )

    return task.to_dict(), 204

@tasks_bp.patch("<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.is_complete = False
    task.completed_at = None

    db.session.commit()

    return task.to_dict(), 204