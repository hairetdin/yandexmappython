# coding: utf-8

import sys
import urllib2
import xml.dom.minidom

reload(sys)
sys.setdefaultencoding('utf8')

GEOCODE_URL = 'http://geocode-maps.yandex.ru/1.x/?geocode='


def get_coords(place_city, address_city):
    request_url = GEOCODE_URL + place_city + address_city
    response = urllib2.urlopen(request_url)
    try:
        dom = xml.dom.minidom.parseString(response.read())
        pos_elem = dom.getElementsByTagName('pos')[0]
        pos_data = pos_elem.childNodes[0].data
        return tuple(pos_data.split())
    except IndexError:
        return None, None


def get_map(place_city, address_city):
    coords = get_coords(place_city, address_city)
    map_js = u"""
        ymaps.ready(init);

        function init() {
            var myMap = new ymaps.Map("map", {
                    center: [%s, %s],
                    zoom: 17
                }, {
                    searchControlProvider: 'yandex#search'
                });

            myMap.geoObjects
                .add(new ymaps.Placemark([%s, %s], {
                    balloonContent: '<strong>%s</strong>'
                }, {
                    preset: 'islands#icon',
                    iconColor: '#0095b6'
                }));
        }
        """ % (coords[1], coords[0], coords[1], coords[0], address_city)
        ya_map_api_js = '<script src="http://api-maps.yandex.ru/2.1/?lang=ru_RU" type="text/javascript"></script>'
    return '{}<script>{}</script>'.format(ya_map_api_js, map_js)


if __name__ == "__main__":
    #получаем широту и долготу
    place_city = u'Уфа'
    address_city = u'Проспект Октября, 1'
    pos = _get_coords(place_city, address_city)
    address = '{}, {}'.format(place_city, address_city)
    print '{} - {}'.format(address, pos)

"""
from get_position import get_map
place_city = u'Уфа'
address_city = u'Проспект Октября, 1'
js_map = get_map(place_city, address_city)
print(js_map)
"""
