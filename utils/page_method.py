from flask import request


def page_method(Model, **extra):
    page = request.args.get('page')
    limit = request.args.get('limit')

    pag_obj = Model.get_all(
        page=page,
        limit=limit,
        **extra,
    )

    return {
        'items': pag_obj.items,
        'total': pag_obj.total,
        'page': page,
    }
