from python_usrus_bot.network.Network import NetworkManager
import json

HOST = "https://yandex.ru/images/search"


async def find_pictures(text):
    manager = NetworkManager.build_url(HOST, path='', params={'text': text})
    builder = await NetworkManager.get_html(manager)
    builder.filterClass('Root')
    builder.filterID('ImagesApp')
    response = builder.build()
    data = json.loads(response[0].get_attribute("data-state"))
    images = []
    for item in data['initialState']['serpList']['items']['entities'].values():
        images.append(item['origUrl'])
    return images
