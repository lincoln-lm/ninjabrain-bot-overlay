from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from aiosseclient import aiosseclient

app = FastAPI()

NINJABRAIN_BOT_URL = "http://localhost:52533"


@app.get("/{path:path}")
async def sse_proxy(request: Request):
    print(f"{NINJABRAIN_BOT_URL}{request.url.path}")

    async def event_stream():
        async for event in aiosseclient(f"{NINJABRAIN_BOT_URL}{request.url.path}"):
            yield f"data: {event}\n\n"

    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "text/event-stream",
        "Access-Control-Allow-Origin": "*",
    }

    return StreamingResponse(event_stream(), headers=headers)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=52534)
