import hashlib

from fastapi import FastAPI
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request


EMAIL = "23f2004096@ds.study.iitm.ac.in"


mcp = FastMCP(
    "Challenge MCP Server"
)


@mcp.tool
def solve_challenge() -> str:

    request = get_http_request()

    challenge = request.headers.get(
        "X-Exam-Challenge"
    )

    if not challenge:
        return "missing_challenge"


    normalized_email = EMAIL.strip().lower()

    text = f"{challenge}:{normalized_email}"

    digest = hashlib.sha256(
        text.encode()
    ).hexdigest()

    return digest[:16]



app = FastAPI()


@app.get("/")
def root():
    return {
        "status": "running"
    }


mcp_app = mcp.http_app(
    transport="streamable-http",
    path="/mcp"
)


app.mount(
    "",
    mcp_app
)