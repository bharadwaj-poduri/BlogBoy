from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from Config.service_app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())


@manager.option('-h', '--host', dest='host', default='127.0.0.1')
@manager.option('-p', '--port', dest='port', type=int, default=5000)
@manager.option('-w', '--workers', dest='workers', type=int, default=3)
def gunicorn(host, port, workers):
    """Start the Server with Gunicorn"""
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            return {
                'bind': '{0}:{1}'.format(host, port),
                'workers': workers
            }

        def load(self):
            return app

    application = FlaskApplication()
    return application.run()

@manager.command
def ipython():
    """Starts IPython shell instead of the default Python shell."""
    import sys
    import IPython
    from flask.globals import _app_ctx_stack
    app = _app_ctx_stack.top.app

    banner = 'Python %s on %s\nIPython: %s\n' % (
        sys.version,
        sys.platform,
        IPython.__version__
    )

    ctx = {}
    ctx.update(app.make_shell_context())

    IPython.embed(banner1=banner, user_ns=ctx)

@manager.command
def dbshell():
    """Postgresql Shell"""

    import subprocess
    psql_db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if psql_db_uri:
        subprocess.call(['psql', psql_db_uri])
    else:
        print ('You appear not to have DB URI configured')


if __name__ == '__main__':
    manager.run()
