from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
import uvicorn
import httpx

mcp = FastMCP("nutrition-mcp")

@mcp.tool()
async def get_nutrition(food: str) -> dict:
    """
    Get nutrition facts for a given food using Open Food Facts.

    Args:
        food: Name of the food (e.g., "banana")

    Returns:
        Nutrition info (calories, fat, protein, sugar, etc.)
    """
    search_url = (
        f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={food}"
        f"&search_simple=1&action=process&json=1&page_size=1"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(search_url)
        data = response.json()

        products = data.get("products", [])
        if not products:
            return {"error": "No results found."}

        product = products[0]
        nutriments = product.get("nutriments", {})

        return {
            "product_name": product.get("product_name", "Unknown"),
            "brand": product.get("brands", "Unknown"),
            "calories_kcal": nutriments.get("energy-kcal_100g"),
            "fat_g": nutriments.get("fat_100g"),
            "saturated_fat_g": nutriments.get("saturated-fat_100g"),
            "sugars_g": nutriments.get("sugars_100g"),
            "fiber_g": nutriments.get("fiber_100g"),
            "proteins_g": nutriments.get("proteins_100g"),
            "salt_g": nutriments.get("salt_100g"),
        }

# SSE wrapper
def create_app():
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request):
        async with sse.connect_sse(request.scope, request.receive, request._send) as (read, write):
            await mcp._mcp_server.run(read, write, mcp._mcp_server.create_initialization_options())

    return Starlette(
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ]
    )

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8080)
