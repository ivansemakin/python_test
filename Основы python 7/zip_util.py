
"""
    This is a utility module.

    To use this module, first import it:

    import mark_util

    Use the read_market_all() function to read the data
    on Markets codes:

    FMID_codes,media_codes,location_codes,payment_codes,season_codes,products_codes = read_market_all()
    print(FMID_codes[13])


    Author: Romashov Yurii
    Date: 2/23/2026

"""
import re

# 0 - FMID, 1 - MarketName,
# 2 - Website, 3 - Facebook, 4 - Twitter, 5 - Youtube, 6 - OtherMedia,
# 7 - street, 8 - city, 9 - County, 10 - State, 11 - zip, 
# 12 - Season1Date, 13 - Season1Time, 14 - Season2Date, 15 - Season2Time,
# 16 - Season3Date, 17 - Season3Time, 18 - Season4Date, 19 - Season4Time,
# 20 - x, 21 - y, 22 - Location,
# 23 - Credit, 24 - WIC, 25 - WICcash, 26 - SFMNP, 27 - SNAP,
# 28 - Organic, 29 - Bakedgoods, 30 - Cheese,
# 31 - Crafts, 32 - Flowers, 33 - Eggs, 34 - Seafood,
# 35 - Herbs, 36 - Vegetables, 37 - Honey, 38 - Jams,
# 39 - Maple, 40 - Meat, 41 - Nursery, 42 - Nuts,
# 43 - Plants, 44 - Poultry, 45 - Prepared, 46 - Soap,
# 47 - Trees, 48 - Wine, 49 - Coffee, 50 - Beans,
# 51 - Fruits, 52 - Grains, 53 - Juices, 54 - Mushrooms,
# 55 - PetFood, 56 - Tofu, 57 - WildHarvested, 58 - updateTime

def decomposition(codes):
    """
        decompositon in 6 lists:

        FMID_codes     ->   0 - FMID, 1 - MarketName, 2 - updateTime
        media_codes    ->   0 - Website, 1 - Facebook, 2 - Twitter, 3 - Youtube, 4 - OtherMedia
        location_codes ->   0 - street, 1 - city, 2 - County, 3 - State, 4 - zip, 5 - x, 6 - y, 7 - Location
        payment_codes  ->   0 - Credit, 1 - WIC, 2 - WICcash, 3 - SFMNP, 4 - SNAP
        season_codes   ->   0 - Season1Date, 1 - Season1Time, 2 - Season2Date, 3 - Season2Time, 4 - Season3Date, 5 - Season3Time, 6 - Season4Date, 7 - Season4Time
        products_codes ->   0 - Organic, 1 - Bakedgoods, 2 - Cheese, 3 - Crafts, 4 - Flowers, 5 - Eggs, 6 - Seafood, 7 - Herbs, 8 - Vegetables, 9 - Honey, 10 - Jams,
                            10 - Maple, 11 - Meat, 12 - Nursery, 13 - Nuts, 14 - Plants, 15 - Poultry, 16 - Prepared, 17 - Soap, 18 - Trees, 19 - Wine, 20 - Coffee, 21 - Beans,
                            22 - Fruits, 23 - Grains, 24 - Juices, 25 - Mushrooms, 26 - PetFood, 27 - Tofu, 28 - WildHarvested
    """
    FMID_codes = []
    media_codes = []
    location_codes = []
    payment_codes = []
    season_codes = []
    products_codes = []
    for lines in range(len(codes)):
        FMID_codes.append(codes[lines][0:2])
        FMID_codes[lines].append(codes[lines][58])
        media_codes.append(codes[lines][2:7])
        location_codes.append(codes[lines][7:12])
        location_codes[lines].extend(codes[lines][20:23])
        payment_codes.append(codes[lines][23:28])
        season_codes.append(codes[lines][12:20])
        products_codes.append(codes[lines][28:58])


    return FMID_codes,media_codes,location_codes,payment_codes,season_codes,products_codes

def read_market_all():
    i = 0
    header = []
    codes = []
    data = []


    for line in open('Export.csv').read().split("\n"):
        
        # m = line.strip().replace('"', '').split(",")
        m = line.strip()
        m_ = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', m)
        i += 1
        if i == 1:
            for val in m_:
                header.append(val)
        else:
            data = []
            for idx in range(0, len(m_)):
                if header[idx] == "x" or header[idx] == "y":
                    if m_[idx] != '':
                        val = float(m_[idx])
                    else:
                        pass
                elif m_[idx] == "Y":
                    val = True
                elif m_[idx] == "N" or m_[idx] == "-":
                    val = False
                else:
                    val = m_[idx]
                if type(val)==str and val[-1:]==" ":
                    val = val[:-1]
                if type(val)==str and val.startswith(" "):
                    val = val[1:]
                data.append(val)           
            codes.append(data)
    codes.pop(len(codes)-1)
    return codes


if __name__ == "__main__":
    all_info = read_market_all()
    FMID_codes,media_codes,location_codes,payment_codes,season_codes,products_codes = decomposition(all_info)
    print(FMID_codes)
    # assert len(zip_codes) == 42049, \
    #     f'The number of ZIP codes read is {len(zip_codes)} instead of 42049'
    # print(zip_codes[4108])
    # assert zip_codes[4108] == \
    #     ['12180', 42.673701, -73.608792, 'Troy', 'NY', 'Rensselaer'], \
    #     'Properties of ZIP 12180 are incorrect'
    # print(zip_codes[42048])
    # assert zip_codes[42048] == \
    #     ['99950', 55.542007, -131.432682, 'Ketchikan', 'AK', 'Ketchikan Gateway'], \
    #     'Properties of ZIP 99950 are incorrect'
    # for elem in zip_codes:
    #     assert elem[1] is not None and elem[1] != 0.0, \
    #         f'Latitude of ZIP {elem[0]} is {elem[1]} which is invalid'
    #     assert elem[2] is not None and elem[2] != 0.0, \
    #         f'Latitude of ZIP {elem[0]} is {elem[2]} which is invalid'
    # print('All tests passed!')
