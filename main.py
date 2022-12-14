import argparse
import logging
from logging import Formatter
import sys
from typing import Union

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generator.spotify_generator import SpotifyGenerator
from routes.api import router as api_router
from apscheduler.triggers.cron import CronTrigger
from argparse import Namespace

logoformato = Formatter(fmt="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
root_logger = logging.getLogger()  # no name
for handler in root_logger.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setFormatter(logoformato)
logger = logging.getLogger('main')


def get_application() -> FastAPI:
    application = FastAPI()

    application.include_router(api_router)

    return application


app = get_application()


# sqlite+aiosqlite:///amisadmin.db'
def tick():
    print("Opa foi carai")


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

    parser = argparse.ArgumentParser(description='Run Spotify Generator Server')
    parser.add_argument('--host')
    parser.add_argument('--port')
    parser.add_argument('--cron-hour', dest='cron_hour')
    parser.add_argument('--cron-minute', dest='cron_minute')
    args: Namespace = parser.parse_args()


    def to_int(str_value: Union[str, None]):
        if str_value is None:
            return -1
        return int(str_value)


    def empty_or_default_number(nextval: int, default_value: int):
        logger.info(f"Received... nextval => {nextval} ; default_value => {default_value}")

        if nextval < 0:
            return default_value
        return nextval

    def empty_or_default_str(nextval: Union[str, None], default_value: Union[str, None]):
        logger.info(f"Received... nextval => {nextval} ; default_value => {default_value}")
        if nextval is None:
            return default_value
        return nextval

    port = empty_or_default_number(to_int(args.port), 8080)
    host = empty_or_default_str(args.host, "127.0.0.1")

    cron_hour = empty_or_default_number(to_int(args.cron_hour), 0)
    cron_minute = empty_or_default_number(to_int(args.cron_minute), 30)
    logger.info(f"port: {port};host: {host}; cron_hour: {cron_hour}; cron_minute: {cron_minute}")

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
            'apscheduler.timezone': 'america/sao_paulo',
        })
        generator = SpotifyGenerator()
        logger.info(f"Cron will run on hour {cron_hour} and minute {cron_minute}")
        scheduler.add_job(func=generator.generate, trigger=CronTrigger(hour=cron_hour, minute=cron_minute))
        scheduler.start()


    uvicorn.run(app, port=port, host=host)
