from app import marshmallow


class BaseSchema(marshmallow.ModelSchema):
    dump_only = []
    exclude = []
    load_only = []

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('dump_only', [])
        kwargs.setdefault('exclude', [])
        kwargs.setdefault('load_only', [])
        kwargs['dump_only'] += self.dump_only
        kwargs['exclude'] += self.exclude
        kwargs['load_only'] += self.load_only

        super(BaseSchema, self).__init__(*args, **kwargs)
