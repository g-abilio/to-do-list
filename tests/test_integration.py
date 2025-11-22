import json

def test_create_task_success(client):
    response = client.post("/tasks", data=json.dumps({"description": "New Task"}), content_type="application/json")
    assert response.status_code == 201

    data = json.loads(response.data)
    assert data["description"] == "New Task"
    assert data["completed"] is False

def test_create_task_missing_description(client):
    response = client.post("/tasks", data=json.dumps({}), content_type="application/json")
    assert response.status_code == 400

    data = json.loads(response.data)
    assert "error" in data

def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert json.loads(response.data) == []

def test_update_task(client):
    client.post("/tasks", data=json.dumps({"description": "Task to update"}), content_type="application/json")
    response = client.put("/tasks/1")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["completed"] is True

def test_delete_task(client):
    client.post("/tasks", data=json.dumps({"description": "Task to delete"}), content_type="application/json")
    response = client.delete("/tasks/1")
    assert response.status_code == 204

    response = client.get("/tasks")
    assert json.loads(response.data) == []