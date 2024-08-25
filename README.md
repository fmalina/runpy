# runpy
Execute sandboxed python tasks
https://www.loom.com/share/9d5d89b8b22b414ab68f1981f0fb07de

## Installation
With Python and pip installed, clone this repo and cd into it, then install libraries:

    git clone https://github.com/fmalina/runpy.git
    cd runpy
    # feel free to safely add --break-system-packages on Ubuntu
    pip install -r requirements.txt

Make sure you have Docker installed and running under current user
allowing Python to control it (on *nix systems):

    sudo usermod -aG docker $USER

To run:

    fastapi dev api.py

## Testing

Visit http://127.0.0.1:8000/docs and click Try it out, enter following test examples or similar
in the request body, press execute and look for response body

Example 1:

    {
     "task_type": "execute_code",
     "code": "print('Hello, World!')",
     "resources": {
     "cpu": "2",
     "gpu": "0",
     "ram": "512MB",
     "storage": "1GB"
     }
    }

Output:

    {"output":"Hello, World!\n"}

Example 2:

    {
     "task_type": "execute_code",
     "code": "for i in range(5): print(f'Count {i}')",
     "resources": {
     "cpu": "1",
     "gpu": "0",
     "ram": "256MB",
     "storage": "500MB"
     }
    }

Output:

    {"output":"Count 0\nCount 1\nCount 2\nCount 3\nCount 4\n"}

ALternatively test from the terminal with Curl:

    curl -X 'POST' \
      'http://127.0.0.1:8000/tasks/exec' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
     "task_type": "execute_code",
     "code": "for i in range(5): print(f'\''Count {i}'\'')",
     "resources": {
     "cpu": "1",
     "gpu": "0",
     "ram": "256MB",
     "storage": "500MB"
     }
    }'
