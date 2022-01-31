import os
import subprocess
import tempfile

from jsonrpc import JSONRPCResponseManager, dispatcher
from werkzeug.wrappers import Request, Response

flags = ["-march=native", "-O2", "-std=c++17", "-pthread"]
filename = "main.cpp"


@dispatcher.add_method
def execute(source: str) -> dict:
    os.chdir(tempfile.mkdtemp())
    with open(filename, "w") as f:
        f.write(source)
    subprocess.run(["g++", *flags, filename])
    result = subprocess.run("./a.out", capture_output=True, timeout=10)
    limit = 1000
    return result.stdout[:limit].decode("utf-8").strip()


@Request.application
def application(request: Request) -> Response:
    response = JSONRPCResponseManager.handle(request.data, dispatcher)

    return Response(response.json, mimetype="application/json")
