import os
import subprocess
import tempfile

from jsonrpc import JSONRPCResponseManager, dispatcher
from werkzeug.wrappers import Request, Response


@dispatcher.add_method
def execute(source: str) -> dict:
    os.chdir(tempfile.mkdtemp())
    with open("main.cpp", "w") as f:
        f.write(source)
    subprocess.run(["g++", "-march=native", "-O2", "main.cpp"])
    result = subprocess.run("./a.out", capture_output=True, timeout=10)
    limit = 1000
    return result.stdout[:limit].decode('utf-8').strip()


@Request.application
def application(request: Request) -> Response:
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)

    return Response(response.json, mimetype="application/json")
