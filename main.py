from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generator.spotify_generator import SpotifyGenerator
from routes.api import router as api_router


def get_application() -> FastAPI:
    application = FastAPI()

    application.include_router(api_router)

    return application


app = get_application()


# sqlite+aiosqlite:///amisadmin.db'
def tick():
    print("Opa foi carai")


@app.on_event("startup")
async def startup_event():
    scheduler = BackgroundScheduler({
        'apscheduler.jobstores.default': {
            'type': 'sqlalchemy',
            'url': 'sqlite:///jobs.sqlite'
        },
        'apscheduler.executors.default': {
            'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
            'max_workers': '20'
        },
        'apscheduler.executors.processpool': {
            'type': 'processpool',
            'max_workers': '5'
        },
        'apscheduler.job_defaults.coalesce': 'false',
        'apscheduler.job_defaults.max_instances': '3',
        'apscheduler.timezone': 'UTC',
    })
    generator = SpotifyGenerator()
    scheduler.add_job(tick, 'interval', seconds=10)
    scheduler.add_job(generator.generate, 'interval', minutes=5)
    scheduler.start()


origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8080, host="127.0.0.1")
