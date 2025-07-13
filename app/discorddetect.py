import httpx

async def fetch_discord_detectable():
    url = "https://discord.com/api/applications/detectable"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")