from flask_apispec import marshal_with as mw, use_kwargs as kw, doc


def api(
    path='/',
    methods=['GET'],
    marshal_with=None,
    use_kwargs=None,
    **wrapkwargs,
):
    def decorator(func):
        new_func = func

        if marshal_with is not None:
            new_func = mw(marshal_with)(new_func)

        if use_kwargs is not None:
            new_func = kw(use_kwargs)(new_func)

        new_func.__docs__ = wrapkwargs
        new_func.__url__ = path
        new_func.__method__ = methods

        return new_func
    return decorator


def register_rules(app, resources):
    for resource in resources:
        for func_name in (d for d in dir(resource) if not d.startswith('__')):
            func = getattr(resource, func_name)


            if hasattr(func, '__url__') and hasattr(func, '__method__'):
                func_url = func.__url__
                func_method = func.__method__
                func_name = func.__name__
                doc_opts = {}

                if hasattr(func, '__docs__'):
                    doc_opts = {
                        **func.__docs__,
                        'tags': [
                            resource.default_tag,
                            *func.__docs__.get('tags', []),
                        ]
                    }

                func = doc(**doc_opts)(func)        
                endpoint = '{}.{}'.format(resource.__name__, func_name)
                app.add_url_rule(
                    resource.base_url + func_url,
                    endpoint=endpoint,
                    view_func=func,
                    methods=func_method,
                    strict_slashes=False,
                )

                app.__docs__.register(func, endpoint=endpoint)
