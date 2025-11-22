import pytest
from app import Task, db

# task creation tests

def test_create_task_success(client):
    res = client.post("/tasks", json={"description": "New task"})
    assert res.status_code == 201

    data = res.get_json()
    assert data["description"] == "New task"
    assert data["completed"] is False
    assert data["id"] is not None

def test_create_task_missing_description(client):
    res = client.post("/tasks", json={})
    assert res.status_code == 400

def test_create_task_empty_description(client):
    res = client.post("/tasks", json={"description": ""})
    assert res.status_code == 400

def test_create_task_stores_long_description_successfully(client):
    long_desc = 'a' * 300
    res = client.post("/tasks", json={"description": long_desc})
    assert res.status_code == 201

    body = res.get_json()
    assert body["description"] == long_desc

def test_create_task_converts_non_string_description_to_string(client):
    res = client.post("/tasks", json={"description": 12345})
    assert res.status_code == 201

    body = res.get_json()
    assert body["description"] == "12345"


def test_create_task_without_json_body(client):
    res = client.post("/tasks")
    assert res.status_code in (400, 415)

def test_create_multiple_tasks(client):
    ids = []
    for i in range(5):
        tid = client.post("/tasks", json={"description": f"Task {i}"}).get_json()["id"]
        ids.append(tid)

    assert ids == sorted(ids)

# task listening tests

def test_list_tasks_when_empty(client):
    res = client.get("/tasks")
    assert res.status_code == 200
    assert res.get_json() == []

def test_list_tasks_after_insert(client):
    client.post("/tasks", json={"description": "Task A"})
    client.post("/tasks", json={"description": "Task B"})
    res = client.get("/tasks")
    assert len(res.get_json()) == 2

def test_list_tasks_should_have_correct_structure(client):
    client.post("/tasks", json={"description": "Structure test"})
    res = client.get("/tasks")
    data = res.get_json()
    assert isinstance(data, list)
    assert {"id", "description", "completed"}.issubset(data[0].keys())

def test_list_tasks_should_return_json_format(client):
    client.post("/tasks", json={"description": "Check JSON"})
    res = client.get("/tasks")
    assert res.is_json

# individual task retrieval tests

def test_list_tasks_returns_all_created_tasks(client):
    client.post("/tasks", json={"description": "A"})
    client.post("/tasks", json={"description": "B"})
    res = client.get("/tasks")
    body = res.get_json()

    assert res.status_code == 200
    assert isinstance(body, list)
    assert len(body) == 2

def test_get_task_invalid_id(client):
    res = client.get('/tasks/999')
    assert res.status_code == 405

# task update tests

def test_update_task_should_mark_task_as_completed(client):
    tid = client.post("/tasks", json={"description": "Update test"}).get_json()["id"]
    res = client.put(f'/tasks/{tid}')

    assert res.status_code == 200
    assert res.get_json()["completed"] is True

def test_update_non_existent_task(client):
    res = client.put('/tasks/555')
    assert res.status_code == 404

def test_update_task_should_be_idempotent(client):
    tid = client.post("/tasks", json={"description": "Idempotent update"}).get_json()["id"]
    client.put(f"/tasks/{tid}")
    res2 = client.put(f"/tasks/{tid}")

    assert res2.get_json()["completed"] is True

def test_update_task_should_not_modify_description(client):
    r = client.post("/tasks", json={"description": "Original text"}).get_json()
    tid = r["id"]
    original_desc = r["description"]
    res = client.put(f"/tasks/{tid}")

    assert res.get_json()["description"] == original_desc

def test_update_task_with_no_body_should_still_work(client):
    tid = client.post("/tasks", json={"description": "No body update"}).get_json()["id"]
    res = client.put(f"/tasks/{tid}")

    assert res.status_code == 200

# task deletion tests

def test_delete_task_success(client):
    tid = client.post("/tasks", json={"description": "Delete me"}).get_json()["id"]
    res = client.delete(f'/tasks/{tid}')

    assert res.status_code == 204

def test_delete_task_should_return_json_body(client):
    tid = client.post("/tasks", json={"description": "Delete body check"}).get_json()["id"]
    res = client.delete(f"/tasks/{tid}")

    assert res.is_json

def test_delete_invalid_task(client):
    res = client.delete('/tasks/123')
    assert res.status_code == 404

def test_delete_then_retrieve(client):
    tid = client.post("/tasks", json={"description": "Temp task"}).get_json()["id"]
    client.delete(f'/tasks/{tid}')
    res = client.get(f'/tasks/{tid}')
    assert res.status_code == 405

def test_delete_task_reduces_task_count(client):
    id1 = client.post("/tasks", json={"description": "X"}).get_json()["id"]
    id2 = client.post("/tasks", json={"description": "Y"}).get_json()["id"]

    before = len(client.get("/tasks").get_json())

    client.delete(f"/tasks/{id1}")

    after = len(client.get("/tasks").get_json())

    assert after == before - 1

# consistency and integrity tests

def test_tasks_should_persist_across_requests_within_same_context(client):
    client.post("/tasks", json={"description": "Persistent A"})
    client.post("/tasks", json={"description": "Persistent B"})
    assert len(client.get("/tasks").get_json()) == 2

def test_task_completed_default_should_be_false(client):
    tid = client.post("/tasks", json={"description": "Default completed"}).get_json()["id"]
    t = Task.query.get(tid)
    assert t.completed is False

def test_ids_should_be_unique_across_tasks(client):
    r1 = client.post("/tasks", json={"description": "Task 1"}).get_json()
    r2 = client.post("/tasks", json={"description": "Task 2"}).get_json()
    assert r1["id"] != r2["id"]

def test_creating_many_tasks(client):
    for i in range(20):
        res = client.post("/tasks", json={"description": f"Bulk {i}"})
        assert res.status_code == 201

# invalid methods and error handling tests

def test_put_on_tasks_collection(client):
    res = client.put("/tasks")
    assert res.status_code in (405, 404)

def test_post_on_task_id_route(client):
    res = client.post('/tasks/1')
    assert res.status_code in (405, 404)

def test_delete_nonexistent_task_returns_404(client):
    res = client.delete("/tasks/999999")
    assert res.status_code == 404

