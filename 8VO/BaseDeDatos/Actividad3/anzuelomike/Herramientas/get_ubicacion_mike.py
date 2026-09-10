from geopy.geocoders import Nominatim

def get_mike_location(lat: float, lon: float):

    geolocator = Nominatim(user_agent="MIKE").reverse((lat, lon))

    return geolocator.address if geolocator else "Ubicación no encontrada"
   


