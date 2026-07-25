import hashlib
from fastapi import FastAPI, Request
from mcp.server.fastmcp import FastMCP


EMAIL = "23f2004096@ds.study.iitm.ac.in"


# Create MCP server
mcp = FastMCP(
    "Challenge MCP Server"
)


@mcp.tool()
def solve_challenge() -> str:
    """
    Solve challenge received from HTTP headers.
    """

    # This will be filled from request context
    request = mcp.get_context().request


    challenge = request.headers.get(
        "X-Exam-Challenge"
    )


    if not challenge:
        return "missing_challenge"


    normalized_email = EMAIL.strip().lower()


    text = (
        challenge
        + ":"
        + normalized_email
    )


    result = hashlib.sha256(
        text.encode()
    ).hexdigest()


    return result[:16]



app = FastAPI()



@app.get("/")
def home():
    return {
        "status": "MCP server running"
    }



# Mount MCP HTTP endpoint

app.mount(
    "/mcp",
    mcp.streamable_http_app()
)