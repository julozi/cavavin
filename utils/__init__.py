# coding=utf-8


def list_routes(app, methods_filter, route_filter):
    """Return registered route of app
    """

    mfilters = methods_filter.split(',')

    try:
        from termcolor import colored
    except:
        def colored(*args, **kargs):
            return args[0]

    EXPAND = 8

    def rule_route(rule):
        if rule.map is None:
            return '<%s (unbound)>' % rule.__class__.__name__
        charset = rule.map is not None and rule.map.charset or 'utf-8'
        tmp = []
        lexpand = 0
        for is_dynamic, data in rule._trace:
            if is_dynamic:
                tmp.append(colored('%s' % (data), attrs=['underline']))
                lexpand += EXPAND
            else:
                tmp.append(data)
        return ['%s' % (u''.join(tmp).encode(charset).lstrip('|')), lexpand]

    output = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            for method in rule.methods:
                if method in mfilters:
                    ruler = rule_route(rule)
                    if (not route_filter) or (route_filter and route_filter in ruler[0]):
                        route = {'method': method, 'route': ruler[0], 'route_expanded_length': ruler[1],
                                 'endpoint': rule.endpoint, 'doc': app.view_functions[rule.endpoint].__doc__}
                        output.append(route)

    return output


def drop_all_tables(app):
    """ Drop all tables, regardless of cascading """

    from cavavin.extensions import db

    engine = db.get_engine(app).name
    if engine == 'postgresql':
        sql_raw_query = 'select \'drop table if exists "\' || tablename || \'" cascade;\' from pg_tables where schemaname=\'public\';'
        for result in db.engine.execute(sql_raw_query):
            db.engine.execute(result[0])
    elif engine == 'sqlite':
        db.drop_all()
