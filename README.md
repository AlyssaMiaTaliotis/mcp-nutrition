# Nutrition MCP Server 🥗

This is a [Model Context Protocol (MCP)](https://modelcontextprotocol.org) compatible server that provides **nutrition facts** for any food using the **Open Food Facts** API.

It enables AI models or agents to call a simple tool and get back calories, macros, and other useful dietary information.

---

## 🛠️ Tool: `get_nutrition` 🥝

```python
get_nutrition(food: str) → dict

## Example Call 
{
  "food": "banana"
}

## Returns
{
  "product_name": "Organic Banana",
  "brand": "Whole Foods",
  "calories_kcal": 89,
  "fat_g": 0.3,
  "saturated_fat_g": 0.1,
  "sugars_g": 12.2,
  "fiber_g": 2.6,
  "proteins_g": 1.1,
  "salt_g": 0
}
