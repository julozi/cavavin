# coding=utf-8

from flask.ext.script import Manager

from cavavin.app import create_app, db

app = create_app()
manager = Manager(app)


@manager.command
def create_tables(clean=False):
    """ Create all tables.
    Add -c or --clean if you want to remove existing tables
    """

    # Drop tables
    if clean:
        app.logger.info("Dropping all tables...")
        from utils import drop_all_tables
        drop_all_tables(app)

    # Create tables
    app.logger.info("Creating all tables...")
    import cavavin.models  # NOQA: to register all Model
    db.create_all()


@manager.option('-m', '--methods', dest='methods_filter', default='GET,DELETE,PUT,POST')
@manager.option('-f', '--filter', dest='route_filter', default=None)
def routes(methods_filter, route_filter):
    """ List routes of application """
    from utils import list_routes

    app_routes = list_routes(app, methods_filter, route_filter)
    if app_routes:
        for line in sorted(app_routes):
            print("{:8s} {:{width}s} {}".format(line['method'], line['route'], line['endpoint'],
                                                width=70 + line['route_expanded_length']))
    else:
        print("No route !")


if __name__ == "__main__":
    manager.run()
