from get_data import *

def get_user_value(user_id):
    try:
        with open("user.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(":")
                if len(parts) == 2 and parts[0] == str(user_id):
                    return parts[1]
        print(f"{user_id}을 검색하였으나 없음")
        return None
    except Exception as e:
        print(e)
        return None

def update_user_value(user_id, new_value):
    try:
        if check_baekjoon_id(new_value) == False:
            return None
        
        lines = []
        updated = False
        
        with open("user.txt", "r") as file:
            lines = file.readlines()
        
        with open("user.txt", "w") as file:
            for line in lines:
                parts = line.strip().split(":")
                if len(parts) == 2 and parts[0] == str(user_id):
                    file.write(f"{user_id}:{new_value}\n")
                    updated = True
                else:
                    file.write(line)
        
        if updated:
            print(f"User value for ID {user_id} updated to {new_value} successfully.")
        else:
            print(f"No user with ID {user_id} found.")
            with open("user.txt", "a") as file:
                file.write(f"{user_id}:{new_value}\n")
            print(f"User value for ID {user_id}: {new_value} saved successfully.")
        return 1
    except Exception as e:
        print(e)

def check_baekjoon_id(baekjoon_id):
    link = "https://www.acmicpc.net/user/" + baekjoon_id
    if baekjoon(link).find("span","error-v1-title"): #아이디 존재 안하면 false 을 return
        return False
    else:
        return True