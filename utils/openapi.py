from flask_apispec import marshal_with as mw, use_kwargs as kw, doc
from utils import http_status


def api(
    path='/',
    methods=['GET'],
    marshal_with=None,
    success_code=http_status.HTTP_200_OK,
    use_kwargs=None,
    not_in_prod_doc=False,
    **wrapkwargs,
):
    def decorator(func):
        new_func = func

        if marshal_with is not None:
            new_func = mw(marshal_with, code=success_code)(new_func)

        if use_kwargs is not None:
            new_func = kw(use_kwargs)(new_func)

        if hasattr(new_func, '__docs__'):
            new_func.__docs__ = {
                **new_func.__docs__,
                **wrapkwargs,
            }
        else:
            new_func.__docs__ = wrapkwargs

        new_func.__url__ = path
        new_func.__method__ = methods
        new_func.__not_in_prod_doc__ = not_in_prod_doc

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
                not_in_prod_doc = func.__not_in_prod_doc__

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

                is_dev = app.config['FLASK_ENV'] == 'development'
                if is_dev or (is_dev == False and not_in_prod_doc == False):
                    app.__docs__.register(func, endpoint=endpoint)

    for key, value in app.__docs__.spec._paths.items():
        app.__docs__.spec._paths[key] = {
            inner_key: inner_value
            for inner_key, inner_value in value.items()
            if inner_key != 'options'
        }
