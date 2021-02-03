from math import sin, cos, sqrt, atan2, radians

def get_distance_to_object(user_location, target_location):
  # approximate radius of earth in km
  R = 6373.0

  lat1 = radians(user_location['lat'])
  lon1 = radians(user_location['lon'])
  lat2 = radians(target_location['lat'])
  lon2 = radians(target_location['lon'])

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))

  distance = R * c * 1000

  return distance

loc1 = {'lat': 52.2296756, 'lon': 21.0122287}
loc2 = {'lat': 52.406374, 'lon': 16.9251681}

print(get_distance_to_object(loc1, loc2))