import requests
import uuid

ENDPOINT = "https://todo.pixegami.io/"

def test_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200




def test_create_and_get_task():
    payload=new_task_payload()
    response = create_task(payload)
    assert response.status_code==200

    data = response.json()
    print(data)

    task_id =data["task"]["task_id"]
    get_task_response = get_task(task_id)
    assert get_task_response.status_code==200

    get_task_data = get_task_response.json()
    print(get_task_data)
    assert get_task_data["content"]== payload["content"]
    assert get_task_data["user_id"]== payload["user_id"]


def test_update_task():
    #creat task
    payload=new_task_payload()
    response = create_task(payload)
    assert response.status_code==200
    task_id = response.json()["task"]["task_id"]
    
    #update task
    new_payload={
    "content": "new",
    "user_id": payload["user_id"],
    "task_id": task_id,
    "is_done": True,
    }
    update_response = update_task(new_payload)
    assert update_response.status_code == 200

    #get and validate the changes
    get_task_response= get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"]== new_payload["content"]
    assert get_task_data["user_id"]== new_payload["user_id"]

def test_list_users():
    #create N tasks
    n=3
    payload= new_task_payload()
    for _ in range(n):
        create_task_response=create_task(payload)
        assert create_task_response.status_code==200


    #list tasks and chech if there are n tasks
    user_id=payload["user_id"]
    list_task_response=list_tasks(user_id)
    assert list_task_response.status_code == 200
    data=list_task_response.json()
    tasks=data["tasks"]
    assert len(tasks) == n

def test_delete_task():
    #create a task
    payload=new_task_payload()
    response = create_task(payload)
    assert response.status_code==200
    task_id = response.json()["task"]["task_id"]

    #delete a task
    delete_task_response=delete_task(task_id)
    assert delete_task_response.status_code==200

    #get task and check its not found
    get_task_response=get_task(task_id)
    assert get_task_response.status_code==404




# helper functions #

def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}" )

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}" )

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}" )

def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}" 
    content = f"test_user_{uuid.uuid4().hex}"  
    #hex turn it into string we used uuid to avoid assigning all the task to same user_id
    return{
  "content": content,
  "user_id": user_id,
  "task_id": "string",
  "is_done": False,

    }