import hashlib

from fastapi import FastAPI, Request
from mcp.server.fastmcp import FastMCP


EMAIL = "23f2004096@ds.study.iitm.ac.in"


mcp = FastMCP(
    "Challenge MCP Server"
)


@mcp.tool()
def solve_challenge():
    request = mcp.get_context().request

    challenge = request.headers.get(
        "X-Exam-Challenge"
    )

    if not challenge:
        return "missing_challenge"

    normalized_email = EMAIL.strip().lower()

    value = (
        challenge
        + ":"
        + normalized_email
    )

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


# IMPORTANT: keep /mcp
app.mount(
    "/mcp",
    mcp.streamable_http_app()
)