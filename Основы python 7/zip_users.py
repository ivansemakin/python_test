import math

# line = "0,0,1,2,0,0,1,0"
# cells = line.split(',')
# cells1 = [[int(numb) for numb in cells] ]
# print(cells1)
# cells2 = [int(item.strip()) for item in cells if item.strip()]
# print(cells2)

import csv
import hashlib,os


LIMIT_IDS_ON_PAGE = 10


def add_user_to_csv(filename, username, password, is_admin):

    """
    Writes user data to a CSV file, checking for the user's existence.
    The password is saved as an MD5 hash.
    
    """
    # Проверяем, существует ли пользователь с таким ником
    if os.path.isfile(filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None) 
            for row in reader:
                if row and row[0] == username:
                    return False

    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    
    file_exists = os.path.isfile(filename)
    headers = ["User", "Hash-password", "AdminRights"]
    new_row = [username, hashed_password, is_admin]
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow(new_row)

    return True


def authenticate_user(filename, username, password):
    """
    Checks the login and password.
    Returns True and the access rights if the data is correct; otherwise, False.
    """
    error_code = None
    if not os.path.isfile(filename):
        error_code = 1
        return False, None,error_code,username

    input_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Используем DictReader для доступа по именам колонок
        for row in reader:
            if row["User"] == username:
                if row["Hash-password"] == input_hash:
                    is_admin = row["AdminRights"] == 'True'
                    error_code = 0
                    return True, is_admin, error_code,username
                else:
                    error_code = 2
                    return False, None,error_code,username

    error_code = 3
    return False, None, error_code,username

def find_review_on_market(reviews,page,last_request):
    """
    Find reviews on specific index.
    """
    index = LIMIT_IDS_ON_PAGE * page + int(last_request)-1
    filename = 'users_reviews.csv'
    market_reviews = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row and ( int(row[1]) == index):
                    market_reviews.append(row)
    return market_reviews


def save_market_review(username, marketindex, grade, review=""):
    """
    Write or rewriting review if its already exist.
    """
    filename = 'users_reviews.csv'
    header = ['username', 'marketindex', 'grade', 'review']
    new_entry = [username, marketindex, grade, review]
    
    rows = []

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row and not (row[0] == new_entry[0] and row[1] == new_entry[1]):
                    rows.append(row)


    rows.append(new_entry)

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header) 
        writer.writerows(rows) 

def read_all_reviews():
    """
    Read all reviews from file.
    """
    filename = 'users_reviews.csv'
    rows = []

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                rows.append(row)
        
    return rows

def delete_market_review(username, marketindex):
    """
    Write or rewriting review if its already exist.
    """
    filename = 'users_reviews.csv'
    header = ['username', 'marketindex', 'grade', 'review']
    old_entry = [username, str(marketindex)]
    flag_deleted = False
    
    rows = []

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row and not (row[0] == old_entry[0] and row[1] == old_entry[1]):
                    rows.append(row)

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header) 
            writer.writerows(rows) 
        flag_deleted = True
    return flag_deleted

# tet,tet2,tet3 = authenticate_user("users_info.csv","ryv","Diabolic")

