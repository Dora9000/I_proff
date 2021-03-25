from aiohttp import web
import json


async def get_data_from_request(request):
    try:
        data = await request.text()
        data = json.loads(data)
    except Exception:
        data = await request.post()
    if data.get('content') is None and data.get('title') is None:
        return None
    return data


async def get_id(app):
    app['id'] += 1
    return app['id']


async def set_data_db(app, id, key, val):
    redis_server = app['redis']
    if val is not None:
        await redis_server.hset(id, key, val)


async def get_data_db(app, id, key):
    redis_server = app['redis']
    answer = await redis_server.hget(id, key)
    if answer is None:
        print(answer)
    return answer


async def get_data(app, id=None):
    redis_server = app['redis']
    answer = []
    if id is None:
        ids = await redis_server.keys('*')
        for _id in ids:
            title = await redis_server.hget(_id, 'title')
            content = await redis_server.hget(_id, 'content')
            answer.append({'id': int(_id.decode('ascii')),  # ("utf-8")
                           'title': content.decode('ascii')[:min(app['config']['N'], len(
                               content.decode('ascii')))] if title is None else title.decode('ascii'),
                           'content': content.decode('ascii')})
        return answer
    else:
        title = await redis_server.hget(id, 'title')
        content = await redis_server.hget(id, 'content')
        if content is None and title is None:
            return None
        return {'id': int(id),
                'title': content.decode('ascii')[:min(max(app['config']['N'], 0), len(
                    content.decode('ascii')))] if title is None else title.decode('ascii'),
                'content': content.decode('ascii')}


async def notes_get(request):
    filter = request.query.get('query')
    answers = await get_data(request.app)
    if filter is None:
        return web.Response(text=json.dumps(answers), content_type="application/json")
    else:
        filtered_answer = []
        for answer in answers:
            if answer.get('title').find(filter) != -1 or answer.get('content').find(filter) != -1:
                filtered_answer.append(answer)
        return web.Response(text=json.dumps(filtered_answer), content_type="application/json")


async def notes_get_id(request):
    if request.match_info['id'] is None:
        return web.Response(status=404,
                            text=json.dumps({"message": "not found"}),
                            content_type="application/json")
    answers = await get_data(request.app, id=request.match_info['id'])
    if answers is None:
        return web.Response(status=404,
                            text=json.dumps({"message": "not found"}),
                            content_type="application/json")
    return web.Response(text=json.dumps(answers), content_type="application/json")


async def notes_post(request):
    data = await get_data_from_request(request)
    if data is None or data.get('content') is None:
        return web.Response(status=405,
                            text=json.dumps({"message": "wrong params"}),
                            content_type="application/json")

    new_id = await get_id(request.app)
    await set_data_db(app=request.app, id=new_id, key='title', val=data.get('title'))
    await set_data_db(app=request.app, id=new_id, key='content', val=data.get('content'))
    answer = {"id": int(new_id), "content": data.get('content')}
    if data.get('title') is not None:
        answer["title"] = data.get('title')
    return web.Response(text=json.dumps(answer), content_type="application/json")


async def notes_delete(request):
    if request.match_info['id'] is None:
        return web.Response(status=405,
                            text=json.dumps({"message": "wrong params"}),
                            content_type="application/json")
    try:
        s = await request.app['redis'].delete(request.match_info['id'])
        if s == 0:
            return web.Response(status=404,
                                text=json.dumps({"message": "not found"}),
                                content_type="application/json")
    except Exception as e:
        print(e)
        return web.Response(status=403)
    return web.Response(text=json.dumps({"message": "ok"}), content_type="application/json")


async def notes_put_id(request):
    new_id = request.match_info['id']
    if new_id is None:
        return web.Response(status=405,
                            text=json.dumps({"message": "wrong params"}),
                            content_type="application/json")
    answers = await get_data(request.app, id=new_id)
    if answers is None:
        return web.Response(status=404,
                            text=json.dumps({"message": "not found"}),
                            content_type="application/json")
    data = await get_data_from_request(request)
    if data is None:
        return web.Response(status=405,
                            text=json.dumps({"message": "wrong params"}),
                            content_type="application/json")

    await set_data_db(app=request.app, id=new_id, key='title', val=data.get('title'))
    await set_data_db(app=request.app, id=new_id, key='content', val=data.get('content'))
    answer = {"id": int(new_id)}
    if data.get('title') is not None:
        answer["title"] = data.get('title')
    if data.get('content') is not None:
        answer["content"] = data.get('content')
    return web.Response(text=json.dumps(answer), content_type="application/json")
