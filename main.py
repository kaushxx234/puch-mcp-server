from typing import Annotated
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
import markdownify
from mcp import ErrorData, McpError
from mcp.server.auth.provider import AccessToken
from mcp.types import INTERNAL_ERROR, INVALID_PARAMS, TextContent
from pydantic import AnyUrl, Field
import readabilipy

TOKEN = "f6dd6073e8ff"  # Puch application key
MY_NUMBER = "919511390234"   # your phone number with country code (without +)


# Auth Provider
class SimpleBearerAuthProvider(BearerAuthProvider):
    def __init__(self, token: str):
        k = RSAKeyPair.generate()
        super().__init__(
            public_key=k.public_key, jwks_uri=None, issuer=None, audience=None
        )
        self.token = token

    async def load_access_token(self, token: str) -> AccessToken | None:
        if token == self.token:
            return AccessToken(
                token=token,
                client_id='unknown',
                scopes=[],
                expires_at=None
            )
        return None


# Puch server instance
mcp = FastMCP("My MCP Server", auth=SimpleBearerAuthProvider(TOKEN))


# Resume tool
@mcp.tool(description=ResumeToolDescription.model_dump_json()) 
async def resume() -> str:
    """
    Return your resume in plain markdown text.
    """
    with open("resume.pdf", "rb") as f:
        # normally you'd extract text here
        # or convert PDF to text first
        text = extract_pdf_text("resume.pdf")  # <- implement this
    return text


# Validation tool
@mcp.tool
async def validate():
    """Validation tool for Puch."""
    return MY_NUMBER


# (Optionally, you can leave fetch tool)


# Run the server
async def main():
    await mcp.run_async("streamable-http", host='0.0.0.0', port=8085)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main()) 
