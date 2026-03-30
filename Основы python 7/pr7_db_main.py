# main.py

import math
import numpy as np
import db_util
import view_console as view
import re
import getpass

# Константы
LIMITED_IDS_ON_PAGE = 10
FORBIDDEN_PATTERN = r'[(){}[\]|`¬¦!«£$%^&*»<>:;#~_\-+=,@]'


def limited_of_markets_page(request, limited_ids, page):
    """Проверка выхода за пределы страницы"""
    if request + page * LIMITED_IDS_ON_PAGE > limited_ids or request < 0:
        return 0, True
    else:
        return page, False


def limit_pages(length):
    """Вычисление количества страниц"""
    if length == 0:
        return 0
    if length % LIMITED_IDS_ON_PAGE == 0:
        return (length // LIMITED_IDS_ON_PAGE) - 1
    else:
        return int(length / LIMITED_IDS_ON_PAGE)


def find_median_grade(market_reviews):
    """Вычисление средней оценки"""
    if not market_reviews:
        return "-"
    else:
        grades = [review[2] for review in market_reviews if review[2] is not None]
        if not grades:
            return "-"
        return sum(grades) / len(grades)


def sort_id_to_index(sort_id, flag_dist=False):
    """Определение индекса для сортировки"""
    if flag_dist:
        view.print_sorting_by_dist()
        return 1  # индекс расстояния в списке markets
    else:
        if sort_id == "3":
            view.print_sorting_by_city()
            return 8  # city
        elif sort_id == "4":
            view.print_sorting_by_state()
            return 10  # state
        elif sort_id == "5":
            view.print_sorting_by_zip()
            return 11  # zip
        else:
            view.print_unknown_command()
            return None


def sorting_menu_dist(dist_info, sort_id):
    """Сортировка списка рынков по расстоянию"""
    flag_dist = True
    view.print_destination()
    index_of_find = sort_id_to_index(sort_id, flag_dist)
    if index_of_find is None:
        return dist_info

    destination = input().strip()
    if destination == "1":
        sorted_data = sorted(dist_info, key=lambda x: x[index_of_find])
    elif destination == "2":
        sorted_data = sorted(dist_info, key=lambda x: x[index_of_find], reverse=True)
    else:
        view.print_destination_error()
        sorted_data = dist_info

    return sorted_data


def sorting_menu_info(all_markets_data, sort_id):
    """Сортировка всех рынков по различным критериям"""
    flag_dist = False
    index_of_find = sort_id_to_index(sort_id, flag_dist)
    if index_of_find is None:
        return all_markets_data

    view.print_destination()
    destination = input().strip()

    if destination == "1":
        sorted_data = sorted(all_markets_data, key=lambda x: x[index_of_find].title() if x[index_of_find] is not None else '')
    elif destination == "2":
        sorted_data = sorted(all_markets_data, key=lambda x: x[index_of_find].title() if x[index_of_find] is not None else '', reverse=True)
    else:
        view.print_destination_error()
        sorted_data = all_markets_data

    return sorted_data


def option_registration():
    """Регистрация нового пользователя"""
    view.print_username()
    user_name = input().strip()
    
    if re.search(FORBIDDEN_PATTERN, user_name):
        view.print_username_error()
        return
    
    view.print_password()
    user_pass = getpass.getpass()
    
    if re.search(FORBIDDEN_PATTERN, user_pass):
        view.print_password_not_pass()
        return
    
    if db_util.add_user_to_db(user_name, user_pass, False):
        view.print_registration_ended()
    else:
        view.print_registration_error(user_name)


def option_authentication():
    """Аутентификация пользователя"""
    view.print_username_login()
    user_name = input().strip()
    view.print_password_login()
    user_pass = getpass.getpass()
    
    success, is_admin, error_code = db_util.authenticate_user(user_name, user_pass)
    view.print_authenticate(error_code)
    
    if error_code == 0:
        return success, is_admin, user_name
    else:
        return False, False, None


def option_find_markets(flag_user_admin, username):
    """Поиск рынков по местоположению"""
    view.print_city_name()
    city_name = input().strip()
    if re.search(FORBIDDEN_PATTERN, city_name):
        view.print_city_error()
        return
    
    view.print_state_name()
    state_name = input().strip()
    if re.search(FORBIDDEN_PATTERN, state_name):
        view.print_state_error()
        return
    
    view.print_zip_code()
    zip_name = input().strip()
    if re.search(FORBIDDEN_PATTERN, zip_name):
        view.print_zip_error()
        return
    
    view.print_miles()
    miles_input = input().strip()
    if not miles_input.isdigit():
        view.print_unknown_data()
        return
    
    miles = int(miles_input)
    FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes = db_util.decomposition(db_util.read_market_all())
    markets = db_util.find_markets_by_location(city_name, state_name, zip_name, miles)
    
    if not markets:
        view.print_not_found_markets()
        return
    
    flag_close = False
    flag_sort = False
    page = 0
    current_markets = markets.copy()
    limited_pages = limit_pages(len(markets))
    
    while not flag_close:
        if flag_sort:
            # Меню сортировки
            # view.print_commands_in_sort()


            current_markets = sorting_menu_dist(current_markets, 1)
            limited_pages = limit_pages(len(current_markets))
            page = 0
            flag_sort = False
            # else:
            #     view.print_unknown_command()
            #     flag_sort = False
        else:
            view.print_command_view_markets_by_dist(FMID_codes, page, limited_pages, len(current_markets), current_markets)

            request = input().strip()

            if request == "Close":
                flag_close = True
            elif request == "Sort":
                # markets.sort(key=lambda x: x[1])
                flag_sort = True
            elif request.isdigit():
                idx = int(request) - 1
                if 0 <= idx < LIMITED_IDS_ON_PAGE:
                    market_index = page * LIMITED_IDS_ON_PAGE + idx
                    if market_index < len(current_markets):
                        # FMID_codes[current_markets[market_index][0]][0]
                        view_market_details(FMID_codes[current_markets[market_index][0]][0],username,flag_user_admin)
                        # view_market_details(current_markets[market_index][0])
                else:
                    view.print_index_out_of_range()
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
            # else:
            #     view.print_unknown_command()


def view_market_details(fmid, username=None, is_admin=False):
    """Просмотр детальной информации о рынке"""
    market = db_util.get_market_by_id(fmid)
    if not market:
        view.print_index_out_of_range()
        return
    
    # Декомпозиция для отображения
    FMID_codes = [[market[0], market[1], market[59] if len(market) > 59 else '']]
    media_codes = [market[2:7]]
    location_codes = [market[7:12] + market[20:23]]
    payment_codes = [market[23:28]]
    season_codes = [market[12:20]]
    products_codes = [market[28:58]]
    
    grade = db_util.get_market_grade(fmid)
    
    view.print_all_info_about_market(FMID_codes, media_codes, location_codes, 
                                     payment_codes, season_codes, products_codes, 
                                     1, len(FMID_codes), 0, grade or "-")
    
    # Меню отзывов
    while True:
        view.print_commands_in_info_market()
        choice = input().strip()
        
        if choice == "1":
            break
        elif choice == "2":
            return
        elif choice == "3":
            view_reviews_for_market(fmid, username, is_admin)
        else:
            view.print_unknown_command()


def view_reviews_for_market(fmid, username=None, is_admin=False):
    """Просмотр и управление отзывами"""
    reviews = db_util.find_review_on_market(fmid)
    
    if reviews is None:
        reviews = []
    
    page = 0
    limited_pages = limit_pages(len(reviews))
    
    while True:
        view.print_reviews_on_market(reviews, page, limited_pages, len(reviews))
        view.commands_on_reviews()
        
        choice = input().strip()
        
        if choice == "1":
            break
        elif choice == "2":
            return
        elif choice == "3":
            if username:
                view.print_grade()
                grade_input = input().strip()
                if not (grade_input.isdigit() and 1 <= int(grade_input) <= 5):
                    view.print_grade_error()
                    continue
                
                view.print_review()
                review_text = input().strip()
                
                if re.search(FORBIDDEN_PATTERN, review_text):
                    view.print_review_error()
                    continue
                
                db_util.save_market_review(username, fmid, int(grade_input), review_text)
                view.print_review_saved()
                # Обновляем список отзывов
                reviews = db_util.find_review_on_market(fmid)
                limited_pages = limit_pages(len(reviews))
                page = 0  # Сбрасываем на первую страницу
            else:
                view.print_not_login()
        
        elif choice == "4":
            if username:
                if not reviews:
                    view.print_no_reviews()
                    continue
                    
                view.print_choose_review()
                idx_input = input().strip()
                if idx_input.isdigit():
                    idx = int(idx_input) - 1 + page * LIMITED_IDS_ON_PAGE
                    if 0 <= idx < len(reviews):
                        # Проверяем права на удаление
                        if reviews[idx][0] == username or is_admin:
                            review_id = reviews[idx][5]
                            db_util.delete_market_review(username, review_id, is_admin)
                            view.print_review_deleted()
                            # Обновляем список отзывов
                            reviews = db_util.find_review_on_market(fmid)
                            limited_pages = limit_pages(len(reviews))
                            page = 0  # Сбрасываем на первую страницу
                        else:
                            view.print_not_permisson()
                    else:
                        view.print_incorrect_index_review()
            else:
                view.print_not_login()
        elif choice == "Page":
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
        # elif choice.startswith("P"):
        #     page_part = choice[1:]
        #     if page_part.isdigit():
        #         page_number = int(page_part)
        #         if 0 <= page_number <= limited_pages:
        #             page = page_number
        #         else:
        #             view.print_pages_out_of_range()
        else:
            view.print_unknown_command()


# def all_markets_view(flag_login, flag_user_admin, username):
#     """Просмотр всех рынков"""
#     total_markets = db_util.get_market_count()
#     limited_pages = limit_pages(total_markets)
#     page = 0
#     flag_close = False
#
#     while not flag_close:
#         offset = page * LIMITED_IDS_ON_PAGE
#         markets = db_util.get_markets_paginated(offset, LIMITED_IDS_ON_PAGE)
#
#         if not markets:
#             view.print_not_found_markets()
#             break
#
#         view.print_command_view_markets(markets, page, limited_pages, total_markets)
#
#         request = input().strip()
#
#         if request == "Close":
#             flag_close = True
#         elif request == "Sort":
#             # view.print_unknown_command()
#             flag_sort = True
#         elif request.isdigit():
#             idx = int(request) - 1
#             if 0 <= idx < len(markets):
#                 # Передаем информацию о пользователе в функцию просмотра деталей
#                 view_market_details(markets[idx][0], username, flag_user_admin)
#             else:
#                 view.print_index_out_of_range()
#         elif request.startswith("P"):
#             page_part = request[1:]
#             if page_part.isdigit():
#                 page_number = int(page_part)
#                 if 0 <= page_number <= limited_pages:
#                     page = page_number
#                 else:
#                     view.print_pages_out_of_range()
#         else:
#             view.print_unknown_command()
def all_markets_view(flag_login, flag_user_admin, username):
    """Просмотр всех рынков с возможностью сортировки"""
    # Получаем все данные о рынках
    all_info = db_util.read_market_all()

    if not all_info:
        view.print_not_found_markets()
        return

    # Декомпозиция для отображения
    FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes = db_util.decomposition(
        all_info)

    total_markets = len(FMID_codes)
    limited_pages = limit_pages(total_markets)
    page = 0
    flag_close = False
    flag_sort = False
    current_data = all_info.copy()
    current_FMID = FMID_codes.copy()
    current_media = media_codes.copy()
    current_location = location_codes.copy()
    current_payment = payment_codes.copy()
    current_season = season_codes.copy()
    current_products = products_codes.copy()

    while not flag_close:
        if flag_sort:
            # Меню сортировки
            view.print_commands_in_sort()
            sort_request = input().strip()

            if sort_request == "1":
                flag_sort = False
            elif sort_request == "2":
                flag_close = True
            elif sort_request in ["3", "4", "5"]:
                # Сортируем данные
                current_data = sorting_menu_info(current_data, sort_request)
                # Обновляем декомпозицию после сортировки
                current_FMID, current_media, current_location, current_payment, current_season, current_products = db_util.decomposition(
                    current_data)
                total_markets = len(current_FMID)
                limited_pages = limit_pages(total_markets)
                page = 0
                flag_sort = False
            else:
                view.print_unknown_command()
                flag_sort = False
        else:
            # Отображаем текущую страницу
            offset = page * LIMITED_IDS_ON_PAGE
            markets_on_page = []
            for i in range(offset, min(offset + LIMITED_IDS_ON_PAGE, total_markets)):
                markets_on_page.append([current_FMID[i][0], current_FMID[i][1]])

            view.print_command_view_markets(current_data, page, limited_pages, total_markets)

            request = input().strip()

            if request == "Close":
                flag_close = True
            elif request == "Sort":
                flag_sort = True
            elif request.isdigit():
                idx = int(request) - 1
                if 0 <= idx < len(markets_on_page):
                    market_index = page * LIMITED_IDS_ON_PAGE + idx
                    if market_index < total_markets:
                        view_market_details(current_FMID[market_index][0], username, flag_user_admin)
                else:
                    view.print_index_out_of_range()
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
            else:
                view.print_unknown_command()


def main():
    """Основная функция"""
    flag_end = False
    flag_login = False
    flag_user_admin = False
    username = None
    
    while not flag_end:
        if flag_login:
            view.print_command_starter_with_user()
        else:
            view.print_command_starter_without_user()
        
        request = input().strip()
        
        if request == "5":
            view.print_finished()
            flag_end = True
        elif request == "3":
            all_markets_view(flag_login, flag_user_admin, username)
        elif request == "1":
            option_registration()
        elif request == "2":
            if flag_login:
                flag_login = False
                flag_user_admin = False
                username = None
                view.print_logout()
            else:
                flag_login, flag_user_admin, username = option_authentication()
        elif request == "4":
            option_find_markets(flag_user_admin, username)
        else:
            view.print_unknown_command()


if __name__ == "__main__":
    main()
    