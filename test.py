from samples import *

object = 'Красная площадь'
info = geocode(object)
print(info)
print(get_coordinates(object))
print(get_ll_span(object))
ll, spn = get_ll_span(object)
ll_spn = f"ll={ll}&spn={spn}"
print(ll_spn)
print(get_map_img(ll_spn))