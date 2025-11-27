import json

def test_full_flow(client):
    # create task
    create_res = client.post("/tasks", data=json.dumps({"description": "Test task"}), content_type="application/json")
    assert create_res.status_code == 201

    create_data = json.loads(create_res.data)
    task_id = create_data["id"]

    # verify integrity
    assert create_data["completed"] is False

    # list tasks
    list_res = client.get("/tasks")
    assert list_res.status_code == 200

    tasks = json.loads(list_res.data)
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id

    # update task
    update_res = client.put(f"/tasks/{task_id}")
    assert update_res.status_code == 200

    update_data = json.loads(update_res.data)
    assert update_data["completed"] is True

    # delete task
    delete_res = client.delete(f"/tasks/{task_id}")
    assert delete_res.status_code == 204

    final_list_res = client.get("/tasks")

    # integrity test
    assert json.loads(final_list_res.data) == []

def test_multiple_tasks_interaction(client):
    # create mulitple tasks
    create_res1 = client.post("/tasks", data=json.dumps({"description": "Task 1"}), content_type="application/json")
    create_res2 = client.post("/tasks", data=json.dumps({"description": "Task 2"}), content_type="application/json")
    assert create_res1.status_code == 201
    assert create_res2.status_code == 201
    task2_id = json.loads(create_res2.data)["id"]

    # verify integrity
    list_res = client.get("/tasks")
    tasks = json.loads(list_res.data)
    assert len(tasks) == 2

    # update task and verify integrity
    client.put(f"/tasks/{task2_id}")
    updated_list_res = client.get("/tasks")
    updated_tasks = json.loads(updated_list_res.data)
    assert any(task["completed"] is True for task in updated_tasks)

def test_error_in_flow_missing_description(client):
    # try to create invalid task
    invalid_create_res = client.post("/tasks", data=json.dumps({}), content_type="application/json")
    assert invalid_create_res.status_code == 400
    assert "error" in json.loads(invalid_create_res.data)

    # verify that there is no tasks
    list_res = client.get("/tasks")
    assert json.loads(list_res.data) == []

def test_idempotent_update_in_flow(client):
    # create task
    create_res = client.post("/tasks", data=json.dumps({"description": "Idempotent task"}), content_type="application/json")
    tid = json.loads(create_res.data)["id"]

    # multiple updates
    client.put(f"/tasks/{tid}")
    second_update_res = client.put(f"/tasks/{tid}")
    assert second_update_res.status_code == 200
    assert json.loads(second_update_res.data)["completed"] is True

    # verify completion via listing
    list_res = client.get("/tasks")
    tasks = json.loads(list_res.data)
    assert tasks[0]["completed"] is True

def test_delete_non_existent_in_flow(client):
    # create a task
    create_res = client.post("/tasks", data=json.dumps({"description": "Test task"}), content_type="application/json")
    task_id = json.loads(create_res.data)["id"]

    # try to delete non existent task
    invalid_delete_res = client.delete("/tasks/999")
    assert invalid_delete_res.status_code == 404

    # verification that the real task exists
    list_res = client.get("/tasks")
    tasks = json.loads(list_res.data)
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id