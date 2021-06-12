import time

from ..instances import logger, scheduler

@scheduler.task(
    "interval",
    id="cold_sync",
    weeks=1,
    max_instances=1,
    start_date="2000-01-01 00:00:00",
)
def cold_sync_task():
    with scheduler.app.app_context():
        logger.info("cold sync")

def cold_sync():
    time.sleep(10)
    logger.info('cold sync async')