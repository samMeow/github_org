import queue
import time

import requests
from sqlalchemy.sql.expression import func
from sqlalchemy.dialects.postgresql import insert

from ..instances import logger, scheduler, db
from ..model import GithubOrg
from ..service import GithubService

def cold_sync():
    logger.info('Start Cold sync')
    try:
        max_id = GithubOrg.query.with_entities(func.max(GithubOrg.github_id)).scalar() or 0
        q = queue.Queue()
        q.put(max_id)
        
        while q.not_empty:
            last_id = q.get()
            try:
                data = GithubService.list_orgs(since=last_id, page_size=100)
            except requests.exceptions.HTTPError as e:
                # probaby rate limit
                # rate limit 5000 per hour....
                logger.error(f'error on sync github service {str(e)}')
                time.sleep(600)
                q.put(last_id)
                continue
            if not data:
                break
            stmt = insert(GithubOrg).values([
                {
                    'github_id': datum['id'],
                    'name': datum['login'],
                }
                for datum in data
            ])
            if hasattr(stmt, 'visit_on_conflict_do_update'):
                stmt = stmt.on_conflict_do_update(
                    index_elements=['github_id'],
                    set_={
                        "name": stmt.excluded.name
                    }
                )
            db.session.execute(stmt)
            db.session.commit()
            last = max([ d['id'] for d in data ])
            q.put(last)
    except Exception as e:
        logger.error(str(e), exc_info=True)

# TODO: move to celery for desire behaviour
@scheduler.task(
    "interval",
    id="cold_sync_task",
    weeks=1,
    max_instances=1,
    start_date="2000-01-01 00:00:00",
)
def cold_sync_task():
    with scheduler.app.app_context():
        logger.info('start cold sync task')
        cold_sync()