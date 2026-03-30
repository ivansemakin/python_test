"""
Prompt script for view message in console.
"""

ALL_INFO_COUNT = 60
PRODUCTS = ["Organic", "Bakedgoods", "Cheese", "Crafts", "Flowers", "Eggs", "Seafood", "Herbs", "Vegetables", "Honey", "Jams",\
                        "Maple", "Meat", "Nursery", "Nuts", "Plants", "Poultry", "Prepared", "Soap", "Trees", "Wine", "Coffee", "Beans",\
                        "Fruits", "Grains", "Juices", "Mushrooms", "PetFood", "Tofu", "WildHarvested"]
PAYMENTS = ["Credit","WIC","WICcash","SFMNP","SNAP"]
LIMIT_IDS_ON_PAGE = 10

def commands_on_reviews():
    print("Commands  => \n 1.Back\n 2.Close\n 3.Write review\n 4.Delete review\n For change page write (Exp: P32)\n")

def print_command_starter_without_user():
    print("Commands  => \n 1.Registration\n 2.Login\n 3.View markets\n 4.Find market by loc\n 5.End\n")

def print_command_starter_with_user():
    print("Commands  => \n 1.Registration\n 2.Logout\n 3.View markets\n 4.Find market by loc\n 5.End\n")

def print_index_out_of_range():
    print("Index out of range, try again\n")

# def print_commands_in_review_market():

def find_delimeter(limited_pages,limited_ids,page):
    if page == limited_pages:
        if limited_ids % LIMIT_IDS_ON_PAGE == 0:
            delimiter = LIMIT_IDS_ON_PAGE
        elif limited_ids == 0:
            delimiter = 1
        else:
            delimiter = limited_ids % LIMIT_IDS_ON_PAGE 
    else:
        delimiter = LIMIT_IDS_ON_PAGE
    return delimiter

def print_reviews_on_market(review_info,page,limited_pages,limited_ids):
    if not review_info:
        print("No reviews for this market.\n")
        return
    data = ""
    delimiter = find_delimeter(limited_pages,limited_ids,page)
    for i in range(delimiter):
        data = data +str(i+1)+".User: " + str(review_info[LIMIT_IDS_ON_PAGE*page +i][0]) +" Grade: " + str(review_info[LIMIT_IDS_ON_PAGE*page +i][2]) + " Review: " 
        if review_info[LIMIT_IDS_ON_PAGE*page +i][3]!="":
            data = data + str(review_info[LIMIT_IDS_ON_PAGE*page +i][3]) +"\n"
        else:
            data = data + "No review" +"\n"
    data = data + " Page - " + str(page) +"\n"
    print(data)

def print_sorting_by_dist():
    print("Sorting by distance\n")

def print_sorting_by_city():
    print("Sorting by city\n")

def print_sorting_by_state():
    print("Sorting by state\n")

def print_sorting_by_zip():
    print("Sorting by zip\n")

def print_destination():
    print("Choose destination:\n 1.Up\n 2.Down\n")

def print_destination_error():
    print("Error: taken destination out of commands.Try another command\n")

def print_no_reviews():
    print("No reviews on this market.\n")

def print_commands_in_sort():
    print("Commands  => \n 1.Back\n 2.Close\n 3.Sort by city\n 4.Sort by state\n 5.Sort by zip\n ")


def print_command_view_markets_by_dist(Name_information,page,limited_pages,limited_ids,ids):
    print("Enter 'Page' or 'Sort' or 'Close' or number of market\n")
    data = ""
    delimiter = find_delimeter(limited_pages,limited_ids,page)
    # if page == limited_pages:
    #     if limited_ids%LIMIT_IDS_ON_PAGE == 0:
    #         delimiter = LIMIT_IDS_ON_PAGE
    #     else:
    #         delimiter = limited_ids % LIMIT_IDS_ON_PAGE
    # else:
    #     delimiter = LIMIT_IDS_ON_PAGE
    for i in range(delimiter):
        data = data +str(i+1)+". " + str(Name_information[ids[i+LIMIT_IDS_ON_PAGE*page][0]][1]) +"\n"
    data = data + " Page - " + str(page) 
    print(data)
    
def print_choose_page():
    print("Enter a number of a page\n")
    
def print_command_view_markets(Name_information,page,limited_pages,limited_ids):
    print("Enter 'Page' or 'Sort' or 'Close' or number of market\n")
    data = ""
    delimiter = find_delimeter(limited_pages,limited_ids,page)
    # if page == limited_pages:
    #     if limited_ids%LIMIT_IDS_ON_PAGE == 0:
    #         delimiter = LIMIT_IDS_ON_PAGE
    #     else:
    #         delimiter = limited_ids%LIMIT_IDS_ON_PAGE
    # else:
    #     delimiter = LIMIT_IDS_ON_PAGE
    for i in range(delimiter):
        data = data +str(i+1)+". " + str(Name_information[LIMIT_IDS_ON_PAGE*page +i][1]) +"\n"
    data = data + " Page - " + str(page) 
    print(data)

def print_all_info_about_market_by_index(FMID_codes,media_codes,location_codes,payment_codes,season_codes,products_codes,id,limited_ids):
    if id>limited_ids or id<0:
        print_index_out_of_range()
    else:
        data = ""
        data = data + "FMID - "+ FMID_codes[id][0] + ", MarketName - " + FMID_codes[id][1] + ", updateTime - " + FMID_codes[id][2] + "\n"
        data = data + "Website - "+ media_codes[id][0] + ", Facebook - " + media_codes[id][1] + ", Twitter - " + media_codes[id][2] + ", Youtube - " + media_codes[id][3] + ", OtherMedia - " + media_codes[id][4] + "\n"
        data = data + "street - "+ location_codes[id][0] + ", city - " + location_codes[id][1] + ", County - " + location_codes[id][2] + ", State - " + location_codes[id][3] + ", zip - " \
                + location_codes[id][4] + ", x(float) - " + str(location_codes[id][5]) + ", y(float) - " + str(location_codes[id][6]) + ", Location - " + location_codes[id][7]  + "\n"
        for i in range(len(PAYMENTS)):
            if payment_codes[id] == False:
                data = data + " " + PAYMENTS[i] + " - " + "N, " 
            else:
                data = data + " " + PAYMENTS[i] + " - " + "Y, " 
        data = data + "\n"

        # data = data + "Credit - "+ payment_codes[id][0] + ", WIC - " + payment_codes[id][1] + ", WICcash - " + payment_codes[id][2] + ", SFMNP - " + payment_codes[id][3] + ", SNAP - " + payment_codes[id][4] + "\n"
        data = data + "Season1Date - "+ season_codes[id][0] + ", Season1Time - " + season_codes[id][1] + ", Season2Date - " + season_codes[id][2] + ", Season2Time - " + "\n" + season_codes[id][3] + ", Season3Date - " \
                + season_codes[id][4] + ", Season3Time - " + season_codes[id][5] + ", Season4Date - " + season_codes[id][6] + ", Season4Time - " + season_codes[id][7]  + "\n"
        for i in range(len(PRODUCTS)):
            if products_codes[id] == False:
                data = data + " " + PRODUCTS[i] + " - " + "N, " 
            else:
                data = data + " " + PRODUCTS[i] + " - " + "Y, " 
            if i == 4 or i == 9 or i ==14 or i ==19 or i == 24 or i == 29:
                data = data + "\n"
        print(data)

def print_all_info_about_market(FMID_codes,media_codes,location_codes,payment_codes,season_codes,products_codes,id,limited_ids,page,grade):
    if (id - 1 + page * 10)>limited_ids or id<0:
        print_index_out_of_range()
    else:
        data = ""
        data = data + "FMID - "+ str(FMID_codes[id - 1 + page * 10][0]) + ", MarketName - " + FMID_codes[id - 1 + page * 10][1] + ", updateTime - " + FMID_codes[id - 1 + page * 10][2] + "\n"
        data = data + "Website - "+ str(media_codes[id - 1 + page * 10][0]) + ", Facebook - " + str(media_codes[id - 1 + page * 10][1]) + ", Twitter - " + str(media_codes[id - 1 + page * 10][2]) + ", Youtube - " + str(media_codes[id - 1 + page * 10][3]) + ", OtherMedia - " + str(media_codes[id - 1 + page * 10][4]) + "\n"
        data = data + "street - "+ str(location_codes[id - 1 + page * 10][0]) + ", city - " + str(location_codes[id - 1 + page * 10][1]) + ", County - " + str(location_codes[id - 1 + page * 10][2]) + ", State - " + str(location_codes[id - 1 + page * 10][3]) + ", zip - " \
                + str(location_codes[id - 1 + page * 10][4]) + ", x(float) - " + str(location_codes[id - 1 + page * 10][5]) + ", y(float) - " + str(location_codes[id - 1 + page * 10][6]) + ", Location - " + str(location_codes[id - 1 + page * 10][7]) + "\n"
        for i in range(len(PAYMENTS)):
            if payment_codes[id - 1 + page * 10] == False:
                data = data + " " + PAYMENTS[i] + " - " + "N, " 
            else:
                data = data + " " + PAYMENTS[i] + " - " + "Y, " 
        data = data + "\n"

        # data = data + "Credit - "+ payment_codes[id][0] + ", WIC - " + payment_codes[id][1] + ", WICcash - " + payment_codes[id][2] + ", SFMNP - " + payment_codes[id][3] + ", SNAP - " + payment_codes[id][4] + "\n"
        data = data + "Season1Date - "+ str(season_codes[id - 1 + page * 10][0]) + ", Season1Time - " + str(season_codes[id - 1 + page * 10][1]) + ", Season2Date - " + str(season_codes[id - 1 + page * 10][2]) + ", Season2Time - " + "\n" + str(season_codes[id - 1 + page * 10][3]) + ", Season3Date - " \
                + str(season_codes[id - 1 + page * 10][4]) + ", Season3Time - " + str(season_codes[id - 1 + page * 10][5]) + ", Season4Date - " + str(season_codes[id - 1 + page * 10][6]) + ", Season4Time - " + str(season_codes[id - 1 + page * 10][7]) + "\n"
        for i in range(len(PRODUCTS)):
            if products_codes[id - 1 + page * 10] == False:
                data = data + " " + PRODUCTS[i] + " - " + "N, " 
            else:
                data = data + " " + PRODUCTS[i] + " - " + "Y, " 
            if i == 4 or i == 9 or i ==14 or i ==19 or i == 24 or i == 29:
                data = data + "\n"
        data = data + "Grade: " + str(grade) + "\n"
        print(data)
def print_incorrect_index_review():
    print("Incorrect index of review.Try again.\n")

def print_not_permisson():
    print("Permission denied! You dont have enough rights!\n")

def print_review_deleted():
    print("Review deleted!\n")

def print_review_saved():
    print("Your review saved!\n")

def print_choose_review():
    print("Enter a number of review which u want delete:\n")

def print_grade():
    print("Grade that market (from 1 to 5): ")

def print_not_login():
    print("Permission denied! You are not logged in!\n")

def print_review():
    print("Write a review if you want: ")

def print_grade_error():
    print("Error: grade going beyond boundaries. Try another command.\n")

def print_review_error():
    print("Review using not allowed signs '({[|`¬¦!«£$%^&*»<>:;#~_-+=,@'.\n")

def print_error_in_request():
    print("Input data is incorrect!\n")

def print_pages_out_of_range():
    print("Error: Page is out of range. Try another command\n")

def print_commands_in_info_market():
    print("Commands  => \n 1.Back\n 2.Close\n 3.Reviews\n ")

def print_finished():
    print("Finish\n ")

def print_username():
    print("Enter a username containing only (letters from A to Z and numbers from 0 to 9)\n")

def print_password():
    print("Enter a pasword. Not allowed signs '({[|`¬¦!«£$%^&*»<>:;#~_-+=,@'.\n")

def print_username_error():
    print("Entered username containing not only letters from A to Z and numbers from 0 to 9\n")

def print_password_pass():
    print("Password pass")

def print_password_not_pass():
    print("Password not pass")

def print_registration_ended():
    print(f"Registration is finished succesfull!")

def print_registration_error(username):
    print(f"Error: User named '{username}' already exists! Try again.\n")

def print_username_login():
    print("Enter your username:\n")

def print_password_login():
    print("Enter your password:\n")

def print_authenticate(code):
    if code == 0:
        print("Welcome you're logged in!\n")
    elif code == 1:
        print("Error: 'users_info.csv' not found.\n")
    elif code == 2:
        print("Error: Incorrect password.\n")
    else:
        print("Error: User not found.\n")

def print_city_name():
    print("Enter a city:\n")

def print_state_name():
    print("Enter a state:\n")

def print_zip_code():
    print("Enter a zip:\n")

def print_city_error():
    print("Entered city containing not allowed signs\n")

def print_state_error():
    print("Entered state containing not allowed signs\n")

def print_zip_error():
    print("Entered zip containing not allowed signs\n")

def print_found_index_by_city_error():
    print("Not found market by city,state and zip\n")

def print_not_found_markets():
    print("Not found closest markets.\n")

def print_logout():
    print("LogOut from user.\n")

def print_miles():
    print("Enter a miles.\n")
    
def print_unknown_command():
    print("Unknown command try again\n")

def print_unknown_data():
    print("Data must be positive\n")
