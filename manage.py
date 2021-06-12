import os
import unittest
from pathlib import Path
from dotenv import load_dotenv
import asyncio

ENV = os.getenv('APP_ENV') or 'dev'
env_path = Path('.') / ('.env.' + ENV)
load_dotenv(dotenv_path=env_path)

from app import blueprint
from app.main import create_app
from app.main.tasks import cold_sync

app = create_app(ENV)
app.register_blueprint(blueprint)

app.app_context().push()

# Max 4 MB
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

def with_context(task):
    def run():
        with app.app_context():
            return task()
    return run

@app.cli.command('run')
def run():
    PORT = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=PORT)

@app.cli.command('cold_sync')
def sync():
    asyncio.get_event_loop().run_in_executor(None, with_context(cold_sync))


@app.cli.command('test')
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
