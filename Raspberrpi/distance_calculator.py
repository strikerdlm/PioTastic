import math

def haversine(lat1, lon1, lat2, lon2):
    # Earth radius in meters
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

if __name__ == "__main__":
    # Coordinates from Meshtastic logs
    lat_ed48, lon_ed48 = 4.7316992, -74.0425728
    lat_badbite, lon_badbite = 4.7448064, -74.05568

    distance = haversine(lat_ed48, lon_ed48, lat_badbite, lon_badbite)
    print(f"Distance between !938bed48 and !5919307a: {distance:.2f} meters")

