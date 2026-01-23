import zip_util
import math
import pandas as pd


def distance_point_to_point(latitude_1, latitude_2, longitude_1, longitude_2):
    R_earth_miles = 6371
    phi1, phi2 = math.radians(latitude_1), math.radians(latitude_2)
    dphi = math.radians(latitude_2 - latitude_1)
    dlambda = math.radians(longitude_2 - longitude_1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2   
    central_angle = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R_earth_miles * central_angle * 0.621371


def dms_converter(angle, flag_direction):
    angle_abs = abs(float(angle))
    degrees = int(angle_abs)
    remainder = (angle_abs - degrees) * 60
    minutes = int(remainder)
    seconds = (remainder - minutes) * 60
    if flag_direction:
        direction = '"N' if float(angle) >= 0 else '"S'
    else:
        direction = '"E' if float(angle) >= 0 else '"W'
    angle_dms = f"{degrees:03d}°{minutes:02d}'{seconds:.2f}{direction}"
    return angle_dms


def location_from_zip_code(zip_codes, zip_code):
    finded_data = zip_codes.loc[zip_codes[0] == zip_code].values.tolist()
    if len(finded_data) == 0:
        print(f"Unknown data. Not found {zip_code}")
    else:
        finded_data = finded_data[0]
        latitude_dms = dms_converter(finded_data[1], True)
        longitude_dms = dms_converter(finded_data[2], False)
        print(f'ZIP Code {finded_data[0]} is in {finded_data[3]},{finded_data[4]},{finded_data[5]} county, coordinates: ({latitude_dms},{longitude_dms})')


def zip_codes_from_location(zip_codes, city_name, state_name):
    city_name = city_name.title()
    state_name = state_name.upper()
    print(city_name, state_name)
    finded_data = zip_codes.loc[zip_codes[3] == city_name, zip_codes[4] == state_name].values.tolist()
    if len(finded_data) == 0:
        print(f"Unknown data. Not found {city_name} and {state_name} zip codes.")
    else:
        finded_data = finded_data[0]
        print(f'The following ZIP Code(s) found for {city_name}, {state_name}: {finded_data[0]}')


def distance_from_zips(zip_codes, first_zip, second_zip):
    finded_data1 = zip_codes.loc[zip_codes[0] == first_zip].values.tolist()
    finded_data2 = zip_codes.loc[zip_codes[0] == second_zip].values.tolist()
    if len(finded_data1) == 0 or len(finded_data2) == 0:
        print(f"Unknown data. Not found info about zip codes.")
    else:
        finded_data1 = finded_data1[0]
        finded_data2 = finded_data2[0]
        dist = distance_point_to_point(finded_data1[1], finded_data2[1], finded_data1[2], finded_data2[2])
        print(f'The distance between {finded_data1[0]} and {finded_data2[0]} is {dist:.2f} miles')


zip_codes = zip_util.read_zip_all()
df = pd.DataFrame.from_records(zip_codes)
while True:
    request = input("Command ('loc', 'zip', 'dist', 'end') => ")
    if request == "end":
        print("Done")
        break
    elif request == "loc":
        print(request)
        zip_code = input("Enter a ZIP Code to lookup => ")
        print(zip_code)
        location_from_zip_code(df, zip_code)
    elif request == "zip":
        print(request)
        city_name = input("Enter a city name to lookup => ")
        print(city_name)
        state_name = input("Enter the state name to lookup => ")
        print(state_name)
        zip_codes_from_location(df,city_name, state_name)
    elif request == "dist":
        print(request)
        first_zip_code = input("Enter the first ZIP Code => ")
        print(first_zip_code)
        second_zip_code = input("Enter the second ZIP Code => ")
        print(second_zip_code)
        distance_from_zips(df,first_zip_code, second_zip_code)
    else:
        print("Unknown command, try again.")
