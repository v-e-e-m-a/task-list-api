# import pytest
# from werkzeug.exceptions import HTTPException
# from app.models.goal import Goal
# from app.models.task import Task
# from app.routes.route_utilities import create_model, validate_model

# @pytest.mark.skip(reason="No way to test this feature yet")
# def test_route_utilities_validate_model_with_task(client, three_tasks):
#     #Act
#     task_1 = validate_model(Task, 1)
#     task_2 = validate_model(Task, 2)
#     task_3 = validate_model(Task, 3)

#     #Assert
#     assert task_1.id == 1
#     assert task_1.title == "Water the garden 🌷"
#     assert task_1.description == ""
#     assert task_1.completed_at is None

#     assert task_2.id == 2
#     assert task_2.title == "Answer forgotten email 📧"

#     assert task_3.id == 3
#     assert task_3.title == "Pay my outstanding tickets 😭"


# @pytest.mark.skip(reason="No way to test this feature yet")
# def test_route_utilities_validate_model_with_task_invalid_id(client, three_tasks):
#     #Act & Assert
#     # Calling `validate_model` without being invoked by a route will
#     # cause an `HTTPException` when an `abort` statement is reached 
#     with pytest.raises(HTTPException) as e:
#         result_task = validate_model(Task, "One")
    
#     # Test that the correct status code and response message are returned
#     response = e.value.get_response()
#     assert response.status_code == 400

#     raise Exception("Complete test with an assertion about the response body")
#     # *****************************************************************************
#     # ** Complete test with an assertion about the response body ****************
#     # *****************************************************************************

# @pytest.mark.skip(reason="No way to test this feature yet")
# def test_route_utilities_validate_model_with_task_missing_id(client, three_tasks):
#     #Act & Assert
#     with pytest.raises(HTTPException) as e:
#         result_task = validate_model(Task, 4)
    
#     raise Exception("Complete test with assertion status code and response body")
#     # *****************************************************************************
#     # **Complete test with assertion about status code response body***************
#     # *****************************************************************************

    
# @pytest.mark.skip(reason="No way to test this feature yet")
# def test_route_utilities_validate_model_with_goal(client, one_goal):
#     #Act
#     goal_1 = validate_model(Goal, 1)

#     #Assert
#     assert goal_1.id == 1
#     assert goal_1.title == "Build a habit of going outside daily"

# @pytest.mark.skip(reason="No way to test this feature yet")
# def test_route_utilities_validate_model_with_goal_invalid_id(client, one_goal):
#     #Act & Assert
#     with pytest.raises(HTTPException) as e:
#         result_task = validate_model(Goal, "One")
    
#     raise Exception("Complete test with assertion status code and response body")
#     # *****************************************************************************
#     # **Complete test with assertion about status code response body***************
#     # *****************************************************************************

# @pytest.mark.skip(reason="No way to test this feature yet")
# def test_route_utilities_validate_model_with_goal_missing_id(client, one_goal):
#     #Act & Assert
#     with pytest.raises(HTTPException) as e:
#         result_task = validate_model(Goal, 4)
    
#     raise Exception("Complete test with assertion status code and response body")
#     # *****************************************************************************
#     # **Complete test with assertion about status code response body***************
#     # *****************************************************************************

# @pytest.mark.skip(reason="No way to test this feature yet")
# def test_route_utilities_create_model_with_task(client):
#     #Arrange
#     request_body = {
#         "title": "Make the bed",
#         "description": "",
#         "completed_at": None
#     }

#     #Act
#     response = create_model(Task, request_body)

#     #Assert
#     assert response[0]["id"] == 1 #create_model returns a tuple
#     assert response[0]["title"] == "Make the bed"
#     assert response[0]["description"] == ""
#     assert response[0]["is_complete"] == False
#     assert response[1] == 201

# @pytest.mark.skip(reason="No way to test this feature yet")
# def test_route_utilities_create_model_with_task_missing_title(client):
#     #Arrange
#     request_body = {
#         "description": "",
#         "completed_at": None
#     }
    
#     #Act
#     with pytest.raises(HTTPException) as e:
#         create_model(Task, request_body)
    
#     response = e.value.get_response()
#     assert response.status_code == 400
#     assert response.get_json() == {"details": "Invalid data"}


# @pytest.mark.skip(reason="No way to test this feature yet")
# def test_route_utilities_create_model_with_goal(client):
#     #Arrange
#     request_body = {
#         "title": "Seize the Day!"
#     }

#     #Act
#     response = create_model(Goal, request_body)

#     #Assert
#     assert response[0]["id"] == 1 #create_model returns a tuple
#     assert response[0]["title"] == "Seize the Day!"
#     assert response[1] == 201

# @pytest.mark.skip(reason="No way to test this feature yet")
# def test_route_utilities_create_model_with_goal_missing_title(client):
#     #Arrange
#     request_body = {
#     }
    
#     #Act
#     with pytest.raises(HTTPException) as e:
#         create_model(Goal, request_body)
    
#     raise Exception("Complete test with assertion status code and response body")
#     # *****************************************************************************
#     # **Complete test with assertion about status code response body***************
#     # *****************************************************************************
