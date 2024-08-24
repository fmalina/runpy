import fastapi
import pydantic
import docker


app = fastapi.FastAPI()
docker_client = docker.from_env()


class ResourceSpecs(pydantic.BaseModel):
    cpu: str
    gpu: str
    ram: str
    storage: str


class Task(pydantic.BaseModel):
    task_type: str
    code: str
    resources: ResourceSpecs


@app.post("/tasks/exec")
async def execute_task(task: Task):
    if task.task_type != "execute_code":
        raise fastapi.HTTPException(status_code=400, detail="Invalid task type")

    # Create Docker container with specified resources
    try:
        container = docker_client.containers.run(
            "python:3.9-slim",
            f"python -c \"{task.code}\"",
            detach=True,
            mem_limit=task.resources.ram,
            nano_cpus=int(float(task.resources.cpu) * 1e9),
            volumes={
                '/tmp': {'bind': '/code', 'mode': 'rw'}
            },
            network_disabled=True,
            stderr=True,
            stdout=True
        )
        container.wait()
        output = container.logs().decode("utf-8")
        container.stop()
        container.remove()
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))
    return {"output": output}

