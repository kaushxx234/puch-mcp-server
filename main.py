from typing import Annotated
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
import markdownify
from mcp import ErrorData, McpError
from mcp.server.auth.provider import AccessToken
from mcp.types import INTERNAL_ERROR, INVALID_PARAMS, TextContent
from pydantic import AnyUrl, Field
import readabilipy

TOKEN = "<your_application_key>"  # Puch application key
MY_NUMBER = "<your_phonenumber>"   # your phone number with country code (without +)


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
@mcp.tool
async def resume():
    """Serve your resume as plain markdown text."""
    # Change this path to your own PDF
    from PyPDF2 import PdfReader
    
    with open("resume.pdf", "rb") as f:
        text = ""

        pdf = PdfReader(f)
        for page in pdf.pages:
            text += page.extract_text()
        
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
