import hashlib

from fastapi import FastAPI
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request


EMAIL = "23f2004096@ds.study.iitm.ac.in"


mcp = FastMCP("Challenge MCP Server")


@mcp.tool
def solve_challenge() -> str:
    request = get_http_request()

    challenge = request.headers.get(
        "X-Exam-Challenge"
    )

    if not challenge:
        return "missing_challenge"

    normalized_email = EMAIL.strip().lower()

    value = f"{challenge}:{normalized_email}"

    result = hashlib.sha256(
        value.encode()
    ).hexdigest()

    return result[:16]


app = FastAPI(
    redirect_slashes=False
)


@app.get("/")
def root():
    return {
        "status": "running"
    }


mcp_app = mcp.http_app(
    path="/mcp",
    transport="streamable-http"
)


app.mount(
    "",
    mcp_app
)