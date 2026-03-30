import zip_util, math, statistics
import numpy as np
import view_console as view
import zip_users
import re, os, getpass


FILE_USERS_PATH = 'users_info.csv'
FORBIDDEN_PATTERN = r'[(){}[\]|`¬¦!«£$%^&*»<>:;#~_\-+=,@]'
LIMITED_IDS_ON_PAGE = 10



def limited_of_markets_page(request, limited_ids, page):
    if request + page * LIMITED_IDS_ON_PAGE > limited_ids or request < 0:
        return 0, True
    else:
        return page, False


def limit_pages(lenght):
    if lenght % LIMITED_IDS_ON_PAGE == 0:
        return (lenght // LIMITED_IDS_ON_PAGE) - 1
    else:
        return int(lenght / LIMITED_IDS_ON_PAGE)


def find_median_grade(market_reviews):
    if len(market_reviews) == 0:
        return "-"
    else:
        grades = []
        for i in range(len(market_reviews)):
            grades.append(int(market_reviews[i][2]))
        return statistics.mean(grades)


def distance_to_another_point(latitude_1, latitude_2, longitude_1, longitude_2):
    R_earth_miles = 3958.75
    phi1, phi2 = math.radians(latitude_1), math.radians(latitude_2)
    dphi = math.radians(latitude_2 - latitude_1)
    dlambda = math.radians(longitude_1 - longitude_2)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    central_angle = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R_earth_miles * central_angle


def find_single_market(location_data, city, state, zip_code):
    """
    Ищет подходящие рынки по строгому совпадению штата, города и почтового индекса.
    Возвращает индекс рынка или None, если ничего не найдено.
    """
    indexes = []
    for i in range(len(location_data)):
        if (location_data[i][3] == state and
                location_data[i][1] == city and
                location_data[i][4] == zip_code):
            indexes.append(i)
    return indexes


def find_markets(location_data, city, state, zip_code, max_miles=10):
    """
    Поиск рынков по фильтрам и удаленности.
    """
    matching_ids = []
    indexes_of_comparing_markets = find_single_market(location_data, city, state, zip_code)
    if len(indexes_of_comparing_markets) == 0:
        view.print_found_index_by_city_error()
        return False
    else:
        pass
    market_lat, market_lon = location_data[indexes_of_comparing_markets[0]][5], \
    location_data[indexes_of_comparing_markets[0]][6]
    # print(market_lat, market_lon)
    # Итерируемся по данным рынка (индекс совпадает в обоих массивах)

    for i in range(len(location_data)):
        # print(i)
        # print(location_data[i][5],location_data[i][6])
        if location_data[i][5] != "" and location_data[i][6] != "":
            dist = distance_to_another_point(market_lat, location_data[i][5], market_lon, location_data[i][6])
        else:
            pass
        # print(type(dist),dist)
        if dist <= max_miles:
            matching_ids.append([i, dist])

    return matching_ids


def option_find_markets(FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes,
                        limited_ids):
    flag_close = False
    flag_page = False
    flag_info = False
    flag_sort = False
    flag_out_of_page = False
    view.print_city_name()
    city_name = input()
    if re.search(FORBIDDEN_PATTERN, city_name):
        view.print_city_error()
        return
    else:
        pass
    view.print_state_name()
    state_name = input()
    if re.search(FORBIDDEN_PATTERN, state_name):
        view.print_state_error()
        return
    else:
        pass
    view.print_zip_code()
    zip_name = input()
    if re.search(FORBIDDEN_PATTERN, zip_name):
        view.print_zip_error()
        return
    else:
        pass

    view.print_miles()
    miles = input()
    if miles.isdigit():
        pass
    else:
        view.print_unknown_data()
        return

    data = find_markets(location_codes, city_name, state_name, zip_name, int(miles))

    # print(data)

    if type(data) == bool:
        view.print_not_found_markets()
    elif type(data) == list:
        page = 0
        limited_pages = limit_pages(len(data))
        while not flag_close:
            if not flag_sort:
                if not flag_info:
                    if not flag_page:
                        view.print_command_view_markets_by_dist(FMID_codes, page, limited_pages, len(data), data)
                    else:
                        flag_page = False
                    request = input()
                    if request == "Close":
                        flag_close = True
                    elif request == "Sort":
                        flag_sort = True
                    elif request.isalnum():
                        if request.isdigit():
                            page, flag_out_of_page = limited_of_markets_page(int(request), len(data), page)
                            if not flag_out_of_page:
                                view.print_all_info_about_market_by_index(FMID_codes, media_codes, location_codes,
                                                                          payment_codes, season_codes, products_codes,
                                                                          data[int(request) + page * 10 - 1][0],
                                                                          limited_ids)
                                flag_info = True
                            else:
                                view.print_index_out_of_range()
                                flag_out_of_page = False
                        elif request.startswith("P"):
                            page_part = request[1:]
                            if page_part.isdigit():
                                page_number = int(page_part)
                                if 0 <= page_number <= limited_pages:
                                    page = page_number
                                else:
                                    view.print_pages_out_of_range()
                                    flag_page = True
                            else:
                                view.print_unknown_command()

                        else:
                            view.print_unknown_command()
                    else:
                        view.print_unknown_command()
                else:
                    view.print_commands_in_info_market()
                    request = input()
                    if request == "2":
                        flag_close = True
                    elif request == "1":
                        flag_info = False
                    else:
                        view.print_unknown_command()
            else:
                data = sorting_menu_dist(data, 1)
                flag_sort = False


def option_registration():
    view.print_username()
    user_name = input()
    if re.search(FORBIDDEN_PATTERN, user_name):
        view.print_username_error()
        return
    else:
        pass

    view.print_password()
    user_pass = getpass.getpass()
    if re.search(FORBIDDEN_PATTERN, user_pass):
        view.print_password_not_pass()
        return
    else:
        pass
    flag = zip_users.add_user_to_csv(FILE_USERS_PATH, user_name, user_pass, False)
    if flag:
        view.print_registration_ended()
    else:
        view.print_registration_error(user_name)


def option_authentication():
    view.print_username_login()
    user_name = input()
    view.print_password_login()
    user_pass = getpass.getpass()
    flag_log, flag_adm, error_code, username = zip_users.authenticate_user(FILE_USERS_PATH, user_name, user_pass)
    view.print_authenticate(error_code)
    if error_code == 0:
        return flag_log, flag_adm, username
    else:
        return False, False, username


def in_review_info(reviews, flag_login, flag_user_admin, username, last_page, last_request):
    flag_review = True
    flag_close = False
    flag_error = False
    flag_page = False
    page = 0

    market_reviews = zip_users.find_review_on_market(reviews, last_page, last_request)
    limited_pages = limit_pages(len(market_reviews))
    limited_ids = len(market_reviews)
    while flag_review:
        view.commands_on_reviews()
        if len(market_reviews) == 0:
            view.print_no_reviews()
        else:
            if not flag_page:
                view.print_reviews_on_market(market_reviews, page, limited_pages, limited_ids)
            else:
                flag_page = False
        request = input()
        if request == "2":
            flag_review, flag_close = False, True
        elif request == "1":
            flag_review, flag_close = False, False
        elif request == "3":
            if flag_login:
                view.print_grade()
                grade = input()
                if grade.isdigit() and len(grade) == 1 and int(grade) <= 5 and int(grade) > 0:
                    pass
                else:
                    view.print_grade_error()
                    flag_error = True
                view.print_review()
                user_review = input()
                if re.search(FORBIDDEN_PATTERN, user_review):
                    view.print_review_error()
                    flag_error = True
                if flag_error:
                    view.print_error_in_request()
                    flag_error = False
                else:
                    zip_users.save_market_review(username, str(last_request - 1 + last_page * LIMITED_IDS_ON_PAGE),
                                                 grade, user_review)
                    view.print_review_saved()
                    reviews = zip_users.read_all_reviews()
                    market_reviews = zip_users.find_review_on_market(reviews, last_page, last_request)
                    limited_pages = limit_pages(len(market_reviews))
                    limited_ids = len(market_reviews)
            else:
                view.print_not_login()
        elif request == "4":
            if flag_login:
                view.print_choose_review()
                index = input()
                if index.isdigit() and int(index) <= LIMITED_IDS_ON_PAGE:
                    if market_reviews[int(index) - 1 + LIMITED_IDS_ON_PAGE * page][0] == username or flag_user_admin:
                        zip_users.delete_market_review(username,
                                                       int(last_request) - 1 + LIMITED_IDS_ON_PAGE * last_page)
                        view.print_review_deleted()
                        reviews = zip_users.read_all_reviews()
                        market_reviews = zip_users.find_review_on_market(reviews, last_page, last_request)
                        limited_pages = limit_pages(len(market_reviews))
                        limited_ids = len(market_reviews)
                    else:
                        view.print_not_permisson()
                else:
                    view.print_incorrect_index_review()
            else:
                view.print_not_login()
        elif request == "Page":
            view.print_choose_page()
            request = input()
            if request.isdigit():
                page_number = int(request)
                if 0 <= page_number <= limited_pages:
                    page = page_number
                else:
                    view.print_pages_out_of_range()
                    flag_page = True
            else:
                view.print_unknown_command()
        # elif request.startswith("P"):
        #     page_part = request[1:]
        #     if page_part.isdigit():
        #         page_number = int(page_part)
        #         if 0 <= page_number <= limited_pages:
        #             page = page_number
        #         else:
        #             view.print_pages_out_of_range()
        #             flag_page = True
        #     else:
        #         view.print_unknown_command()
        else:
            view.print_unknown_command()

    return flag_review, flag_close, reviews


def sort_id_to_index(sort_id, flag_dist):
    if flag_dist:
        view.print_sorting_by_dist()
        # sorted_data = sorted(all_info, key=lambda x: x[1])
        index_sort = 1
        return index_sort
    else:
        if sort_id == "3":
            view.print_sorting_by_city()
            index_sort = 8
            return index_sort
        elif sort_id == "4":
            view.print_sorting_by_state()
            index_sort = 10
            return index_sort
        elif sort_id == "5":
            view.print_sorting_by_zip()
            index_sort = 11
            return index_sort
        else:
            view.print_unknown_command()


def sorting_menu_dist(dist_info, sort_id):
    flag_dist = True
    view.print_destination()
    index_of_find = sort_id_to_index(sort_id, flag_dist)
    sorted_data = dist_info
    destination = input()
    if destination == "1":
        sorted_data = sorted(dist_info, key=lambda x: x[index_of_find])
    elif destination == "2":
        sorted_data = sorted(dist_info, key=lambda x: x[index_of_find], reverse=True)
    else:
        view.print_destination_error()

    return sorted_data


def sorting_menu_info(all_info, sort_id):
    FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes = zip_util.decomposition(
        all_info)
    flag_dist = False
    index_of_find = sort_id_to_index(sort_id, flag_dist)
    view.print_destination()
    sorted_data = all_info
    destination = input()
    if destination == "1":
        sorted_data = sorted(all_info, key=lambda x: x[index_of_find])
        FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes = zip_util.decomposition(
            sorted_data)
    elif destination == "2":
        sorted_data = sorted(all_info, key=lambda x: x[index_of_find], reverse=True)
        FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes = zip_util.decomposition(
            sorted_data)
    else:
        view.print_destination_error()

    return sorted_data, FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes


def all_markets_view(FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes, limited_ids,
                     limited_pages, flag_login, flag_user_admin, username, all_info):
    page = 0
    flag_close = False
    flag_info = False
    flag_page = False
    flag_out_of_page = False
    flag_review = False
    flag_sort = False
    reviews = zip_users.read_all_reviews()
    last_request = None

    while not flag_close:
        if not flag_review:
            if not flag_sort:
                if not flag_info:
                    if not flag_page:
                        view.print_command_view_markets(FMID_codes, page, limited_pages, limited_ids)
                    else:
                        flag_page = False
                    request = input()

                    if request == "Close":
                        flag_close = True
                    elif request == "Sort":
                        flag_sort = True
                    elif request.isalnum():
                        if request.isdigit():
                            page, flag_out_of_page = limited_of_markets_page(int(request), limited_ids, page)
                            # print(page,request)
                            if not flag_out_of_page:
                                last_request = int(request)
                                market_reviews = zip_users.find_review_on_market(reviews, page, last_request)
                                grade_of_market = find_median_grade(market_reviews)
                                view.print_all_info_about_market(FMID_codes, media_codes, location_codes, payment_codes,
                                                                 season_codes, products_codes, int(request),
                                                                 limited_ids, page, grade_of_market)

                                flag_info = True
                            else:
                                view.print_index_out_of_range()
                                flag_out_of_page = False
                        elif request == "Page":
                            view.print_choose_page()
                            request = input()
                            if request.isdigit():
                                page_number = int(request)
                                if 0 <= page_number <= limited_pages:
                                    page = page_number
                                else:
                                    view.print_pages_out_of_range()
                                    flag_page = True
                            else:
                                view.print_unknown_command()
                            
                        # elif request.startswith("P"):
                        #     page_part = request[1:]
                        #     if page_part.isdigit():
                        #         page_number = int(page_part)
                        #         if 0 <= page_number <= limited_pages:
                        #             page = page_number
                        #         else:
                        #             view.print_pages_out_of_range()
                        #             flag_page = True
                        #     else:
                        #         view.print_unknown_command()

                        else:
                            view.print_unknown_command()
                    else:
                        view.print_unknown_command()

                else:
                    view.print_commands_in_info_market()
                    request = input()
                    if request == "2":
                        flag_close = True
                    elif request == "1":
                        flag_info = False
                    elif request == "3":
                        flag_review = True
                    else:
                        view.print_unknown_command()
            else:
                view.print_commands_in_sort()
                request = input()
                if request == "2":
                    flag_close = True
                elif request == "1":
                    flag_sort = False
                elif request == "3" or request == "4" or request == "5":
                    all_info, FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes = sorting_menu_info(
                        all_info, request)
                    flag_sort = False
                else:
                    view.print_unknown_command()
                    flag_sort = False

        else:
            flag_review, flag_close, reviews = in_review_info(reviews, flag_login, flag_user_admin, username, page,
                                                              last_request)

    return all_info, FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes


all_info = zip_util.read_market_all()
FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes = zip_util.decomposition(all_info)

# all_info,FMID_codes,media_codes,location_codes,payment_codes,season_codes,products_codes = zip_util.read_market_all()

numpy_all_info = np.array(all_info)
numpy_FMID_codes = np.array(FMID_codes)
numpy_season_codes = np.array(season_codes)
numpy_media_codes = np.array(media_codes)
numpy_location_codes = np.array(location_codes)
numpy_payment_codes = np.array(payment_codes)
numpy_products_codes = np.array(products_codes)
limited_ids = len(FMID_codes)
# print(numpy_FMID_codes[1])
limited_pages = limit_pages(len(FMID_codes))
username = None

# print(limited_pages,limited_ids)
Flag_end = False
flag_user_registration = False
flag_login = False
flag_user_admin = False
while not Flag_end:
    if flag_login:
        view.print_command_starter_with_user()
    else:
        view.print_command_starter_without_user()
    request = input()
    if request == "5":
        view.print_finished()
        Flag_end = True
    elif request == "3":
        all_info, FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes = all_markets_view(
            FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes, limited_ids,
            limited_pages, flag_login, flag_user_admin, username, all_info)
        # zip_code = input()
        # print(zip_code)
        # location_from_zip_code(numpy_zip_codes,zip_code)
    elif request == "1":
        option_registration()
        # view.print_username()
        # user_name = input()
        # view.print_password_pass()
        # user_pass = input()
        # flag_user_registration = zip_users.add_user_to_csv(FILE_USERS_PATH,)
        # if flag_user_registration:
        #     view.print_registration_ended()
        # else:
        #     view.print_registration_error(user_name)
    elif request == "2":
        if flag_login:
            flag_login = False
            flag_user_admin = False
            username = None
            view.print_logout()
        else:
            flag_login, flag_user_admin, username = option_authentication()
    elif request == "4":
        option_find_markets(FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes,
                            limited_ids)
    #     print(request)
    #     city_name = input("Enter a city name to lookup => ")
    #     print(city_name)
    #     state_name = input("Enter the state name to lookup => ")
    #     print(state_name)
    #     zip_codes_from_location(numpy_zip_codes,city_name,state_name)
    # elif request == "dist":
    #     print(request)
    #     first_zip_code = input("Enter the first ZIP Code => ")
    #     print(first_zip_code)
    #     second_zip_code = input("Enter the second ZIP Code => ")
    #     print(second_zip_code)
    #     distance_from_zips(numpy_zip_codes,first_zip_code,second_zip_code)
    else:
        print("Unknown command, try again.")
