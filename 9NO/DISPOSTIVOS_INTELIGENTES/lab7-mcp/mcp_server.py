"""Servidor MCP independiente que consume la API FastAPI de lab7.

Lab7 tiene que estar en marcha antes de arrancar este proceso. Por defecto
lee el OpenAPI en http://127.0.0.1:8000/openapi.json.

Variables de entorno:
    API_BASE_URL   URL de la API (por defecto http://127.0.0.1:8000)
    MCP_API_TOKEN  JWT opcional, enviado como Authorization: Bearer

Uso:
    python mcp_server.py
    python mcp_server.py --http
"""

import os
import sys

import httpx2
from fastmcp import FastMCP
from fastmcp.server.providers.openapi import MCPType, RouteMap

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

headers: dict[str, str] = {}
api_token = os.getenv("MCP_API_TOKEN")
if api_token:
    headers["Authorization"] = f"Bearer {api_token}"

try:
    openapi_spec = httpx2.get(
        f"{API_BASE_URL}/openapi.json",
        headers=headers,
        timeout=10.0,
    ).json()
except httpx2.HTTPError as exc:
    raise SystemExit(
        f"No se pudo leer el OpenAPI de lab7 en {API_BASE_URL}/openapi.json. "
        f"Arranca la API antes que este servidor. Detalle: {exc}"
    ) from exc

client = httpx2.AsyncClient(
    base_url=API_BASE_URL,
    headers=headers,
    timeout=30.0,
)

mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="Lab7 Users",
    route_maps=[
        RouteMap(pattern=r".*/me/profile-pic$", mcp_type=MCPType.EXCLUDE),
    ],
)


def main() -> None:
    if "--http" in sys.argv:
        mcp.run(transport="http", host="127.0.0.1", port=8001, path="/mcp")
        return
    mcp.run()


if __name__ == "__main__":
    main()
