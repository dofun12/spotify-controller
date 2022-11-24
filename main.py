from datetime import date

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_scheduler import SchedulerAdmin

from routes.api import router as api_router


def get_application() -> FastAPI:
    application = FastAPI()

    application.include_router(api_router)

    return application


app = get_application()
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))
scheduler = SchedulerAdmin.bind(site)


@scheduler.scheduled_job('interval', seconds=60)
def interval_task_test():
    print('interval task is run...')


# use when you want to run the job periodically at certain time(s) of day
@scheduler.scheduled_job('cron', hour=3, minute=30)
def cron_task_test():
    print('cron task is run...')


# use when you want to run the job just once at a certain point of time
@scheduler.scheduled_job('date', run_date=date(2022, 11, 11))
def date_task_test():
    print('date task is run...')


@app.on_event("startup")
async def startup():
    # Mount the background management system
    site.mount_app(app)
    # Start the scheduled task scheduler
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

    uvicorn.run(app)
