import json
import asyncio

import aiohttp
from rich.console import Console

console: Console = Console()


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        data: dict[str, str] = {"model": "llama2", "prompt": "why is the sky blue?"}
        async with session.post("http://localhost:11434/api/generate", data=json.dumps(data)) as response:
            while True:
                if response.status != 200:
                    raise RuntimeError()
                chunk: bytes = await response.content.readany()
                if not chunk:
                    break
                console.log(chunk)


if __name__ == "__main__":
    asyncio.run(main())

