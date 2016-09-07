import mapbox_vector_tile


def is_vector_tile(obj):
    try:
        mapbox_vector_tile.decode(obj.read())
    except:
        return False
    return True
