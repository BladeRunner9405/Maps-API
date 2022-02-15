import requests
import sys
import os

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def geocode(address):
    # Собираем запрос для геокодера.
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}" \
                       f"&geocode={address}&format=json"

    # Выполняем запрос.
    response = requests.get(geocoder_request)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
                request=geocoder_request, status=response.status_code, reason=response.reason))

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа он находится по следующему пути:
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


# Получаем координаты объекта по его адресу.
def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return None, None

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Широта, преобразованная в плавающее число:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


# Получаем параметры объекта для рисования карты вокруг него.
def get_ll_span(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и Широта :
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем координаты в параметр ll
    ll = ",".join([toponym_longitude, toponym_lattitude])

    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]

    # левая, нижняя, правая и верхняя границы из координат углов:
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")

    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    # Собираем размеры в параметр span
    span = f"{dx},{dy}"

    return ll, span


# Находим ближайшие к заданной точке объекты заданного типа.
def get_nearest_object(point, kind):
    ll = "{0},{1}".format(point[0], point[1])
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}" \
                       f"&geocode={ll}&kind={kind}&format=json"

    # Выполняем запрос к геокодеру, анализируем ответ.
    response = requests.get(geocoder_request)
    if not response:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {geocoder_request}
            Http статус: {response.status_code,} ({response.reason})""")

    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем первый топоним из ответа геокодера.
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"]["name"] if features else None


def get_map_img(ll_spn=None, map_type="map", add_params=None):
    print(ll_spn, map_type, add_params)
    if ll_spn:
        map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?l={map_type}"

    if add_params:
        map_request += "&" + add_params
    print(map_request)
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    return file
