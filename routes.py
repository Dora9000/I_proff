from aiohttp import web
from functions.default import notes_post, notes_get_id, notes_get, notes_put_id, notes_delete


def setup_routes(app):
    app.router.add_route('POST',
                         '/notes',
                         notes_post,
                         name='notes_post')

    app.router.add_route('GET',
                         '/notes',
                         notes_get,
                         name='notes_get')

    app.router.add_route('GET',
                         r'/notes/{id:\d+}',
                         notes_get_id,
                         name='notes_get_id')

    app.router.add_route('DELETE',
                         r'/notes/{id:\d+}',
                         notes_delete,
                         name='notes_delete')

    app.router.add_route('PUT',
                         r'/notes/{id:\d+}',
                         notes_put_id,
                         name='notes_put_id')
