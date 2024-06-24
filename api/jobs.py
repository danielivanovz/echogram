from threading import Event, Thread
from datetime import datetime
from fastapi import FastAPI
from queue import Queue
from contextlib import asynccontextmanager
from api.config import get_settings
from imap_tools import MailBox, AND

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from api.db.actions import create_email, create_user, get_user_by_email
from api.db.client import create_supabase_client
from api.db.schemas import EmailCreate, UserCreate

job = AsyncIOScheduler(jobstores={"default": MemoryJobStore()}, timezone="UTC")
msg_queue = Queue()

settings = get_settings()
process_event = Event()


@job.scheduled_job("interval", seconds=10)
async def collector_job():
    print(f"Job executed at {datetime.now()}")
    with MailBox(settings.imap_host).login(
        settings.imap_username, settings.imap_password, "INBOX"
    ) as mailbox:
        return [
            (msg_queue.put(EmailCreate.from_msg(msg)), process_event.set())
            for msg in mailbox.fetch(AND(seen=False))
        ]


def run_processor():
    while True:
        process_event.wait()
        while not msg_queue.empty():
            process_email(msg_queue.get())


def process_email(email: EmailCreate):
    print(f"Processing email from {email}")
    client = create_supabase_client()
    user = get_user_by_email(client, email.user_id)

    if not user:
        print(f"User with email {email.user_id} does not exist. Creating user.")
        user = create_user(client, UserCreate(email=email.user_id))

    payload = EmailCreate(user_id=user.user_id, **email.model_dump(exclude={"user_id"}))
    created = create_email(client, payload)
    print(f"Email stored: {created}")
    msg_queue.task_done()
    process_event.clear()


@asynccontextmanager
async def lifespan(_: FastAPI):
    job.start()
    processor_thread = Thread(target=run_processor, daemon=True)
    processor_thread.start()
    try:
        yield
    finally:
        job.shutdown()
        # process_event.set()
        # processor_thread.join()
