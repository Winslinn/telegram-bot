import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

@app.get("/badge")
async def badge():
    svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="84" height="20">
    <!-- Лівий блок: сірий з градієнтом і закругленими лівими кутами -->
    <path d="M3,0 H42 V20 H3 a3,3 0 0 1 -3,-3 V3 a3,3 0 0 1 3,-3 Z" fill="url(#grayGrad)"/>

    <!-- Правий блок: зелений, закруглені тільки праві кути -->
    <path d="M42,0 H81 a3,3 0 0 1 3,3 V17 a3,3 0 0 1 -3,3 H42 V0 Z" fill="url(#greenGrad)"/>

    <!-- Градієнти -->
    <defs>
        <!-- Сірий градієнт -->
        <linearGradient id="grayGrad" x2="0" y2="100%">
        <stop offset="0" stop-color="#555"/>
        <stop offset="1" stop-color="#333"/>
        </linearGradient>

        <!-- Зелений градієнт -->
        <linearGradient id="greenGrad" x2="0" y2="100%">
        <stop offset="0" stop-color="#3c9f3c"/>
        <stop offset="1" stop-color="#2a7f2a"/>
        </linearGradient>
    </defs>

    <!-- Текст -->
    <g fill="#fff" font-family="Verdana,Geneva,sans-serif" font-size="11">
        <text x="21" y="14" text-anchor="middle">Status</text>
        <text x="63" y="14" text-anchor="middle">online</text>
    </g>
    </svg>
    '''
    
    return Response(content=svg, media_type="image/svg+xml")

def run_api():
    print("API is running") 
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
        log_config={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "fmt": "%(asctime)s [%(levelname)s] %(message)s"
                },
            },
            "handlers": {
                "file": {
                    "class": "logging.FileHandler",
                    "filename": "bot/uvicorn.log",
                    "formatter": "default",
                },
            },
            "loggers": {
                "uvicorn": {"handlers": ["file"], "level": "INFO"},
                "uvicorn.error": {"handlers": ["file"], "level": "INFO"},
                "uvicorn.access": {"handlers": ["file"], "level": "INFO"},
            },
        },
    )