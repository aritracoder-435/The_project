import pandas as pd
import os
import json
import time
import sys
import shutil
import time

# ---------------- CLEAR FUNCTION ----------------
def clear_ter():
    os.system('cls' if os.name == 'nt' else 'clear')  # this is for clear terminal

#------------------- title part -----------------
def print_app_title():
    title = " QUIZ APPLICATION "
    border = "═" * (len(title) + 4)
    
    # get terminal width
    term_width = shutil.get_terminal_size().columns
    
    # build lines
    top = f"{border}"
    mid = f"║  {title}  ║"
    bottom = f"{border}"    
    
    # calculate padding for center
    def center_line(line):
        return line.center(term_width)
    
    print(center_line(top))
    print(center_line(mid))
    print(center_line(bottom))


# ---------------- PASSWORD SET FUNCTION ----------------
def set_password(min_length=6):    # default len is 6 
    while True:
        pwd = input("Enter a password: ")

        has_upper = False
        has_lower = False
        has_digit = False
        has_special = False
        has_space = " " in pwd   # 🔹 check for space

        special_chars = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?"

        for ch in pwd:
            if ch.isupper():
                has_upper = True
            elif ch.islower():
                has_lower = True
            elif ch.isdigit():
                has_digit = True
            elif ch in special_chars:
                has_special = True

        pass_length = len(pwd) >= min_length

        if pass_length and has_upper and has_lower and has_digit and has_special and not has_space:
            print("🎉 Password successfully.")
            return pwd   # exit loop when password is correct
        else:
            print("❌ Password is NOT valid.")
            print("   📌 Password must contain:")
            if not pass_length:
                print("    - At least 8 characters")
            if not has_upper:
                print("    - At least one uppercase letter")
            if not has_lower:
                print("    - At least one lowercase letter")
            if not has_digit:
                print("    - At least one digit")
            if not has_special:
                print("    - At least one special character (!@#$ etc.)")
            if has_space:
                print("    - No spaces allowed in the password")
            print("\n⚠ Please try again.\n")


# ---------------- USER HANDLING ----------------
def load_users():
    if os.path.exists("src/dataBase.json"):
        with open("src/dataBase.json", "r") as f:
            return json.load(f)
    # return []


def save_users(users):
    with open("src/dataBase.json", "w") as f:
        json.dump(users, f, indent=4)

#  ------------REGISTER PART-----------------
def register_user():
    user = load_users()

    while True:   # keep asking until unique username
        username = input("Enter username: ")

        # check if username already exists
        if username in user["users_data"]:
            print("❌ This username already exists. Try another one.\n")
        else:
            break   # ✅ unique username found

    password = set_password()   # ✅ this will return the password

    # Add new user with progress
    user["users_data"][username] = {
        "password": password,
        "progress": {
            "time_spent":0,
            "score": 0,
            "attempt":0,
            "correct" : 0,
            "incorrect" : 0,
            "percentage" : 0
        }
        }
    save_users(user)
    print(f"✅ User '{username}' registered successfully!")
    time.sleep(1.5)


#  ------------LOGIN PART-------------------
def login_user():
    print("\n--- Login your account ---")
    user = load_users()
    while True :
        global username
        username = input("Enter username: ")
        if username not in user["users_data"] :
            print("\tuser not found \n\tEnter valid username")
        else:
            break
    while True :
        password = input("Enter password: ")
        if user["users_data"][username]["password"] != password:
            print("password is incorret\nEnter valid password")
        else :
            print("🎉 Login successful! \n")
            time.sleep(1)
            return True  

#  ------------progress-------------------
def update_progrss(duration,score,asked):
    data = load_users()
    sub = data["users_data"][username]["progress"]
    sub["score"] += score
    sub["time_spent"] += duration
    sub["attempt"] += asked
    sub["correct"] += score
    sub["incorrect"] += asked - score
    sub["percentage"] = round((sub["score"])/(sub["attempt"])*100,2)

    save_users(data)


def show_progress():
    data = load_users()
    clear_ter()
    sub = data["users_data"][username]["progress"] # base index
    secound = sub["time_spent"]
    h = secound // 3600
    m = (secound % 3600) // 60
    s = (secound % 60)
    print(f'Hi,{username} ')
    print(f"You spent {h : .0f} hour ,{m : .0f} minute ,{s : .0f} secound in our application")
    print(f"Your score is {sub["score"]}")
    print(f"You attempt total {sub["attempt"]} question")
    print(f"Your given answer is correct for {sub["correct"]} question")
    print(f"Your given answer is incorrect for {sub["incorrect"]} question")
    print(f"Your percentage {sub["percentage"]}%\n")

# ---------------- Leaderboard----------------
def show_leaderboard():
    data = load_users()
    users = data["users_data"]
    if not users :
        print("No user found")
        return
    sorted_users = sorted(users.items(),key = lambda x : x[1]["progress"]["score"],reverse=True)
    print("\n----------------Leaderboard----------------")
    for i,(user,info) in enumerate(sorted_users,start=1):
        print(f"{i}. {user} - {info["progress"]["score"]} points")
    print("")

# ---------------- INPUT WITH TIMEOUT ----------------
def input_with_timeout(prompt, timeout=30):
    print(f"{prompt} (You have {timeout} seconds)")

    start_time = time.time()

    # Windows version
    if sys.platform.startswith("win"):
        import msvcrt
        user_input = ""
        while True:
            remaining = int(timeout - (time.time() - start_time))
            if remaining <= 0:
                print("\n⏰ Time’s up!")
                return None

            print(f"\rTime left: {remaining} seconds | {user_input}", end="", flush=True)

            if msvcrt.kbhit():
                char = msvcrt.getwch()
                if char in ("\r", "\n"):  # Enter key
                    print()
                    return user_input
                elif char == "\b":  # Backspace
                    user_input = user_input[:-1]
                else:
                    user_input += char

            # time.sleep(0.1)



# ---------------- QUIZ SYSTEM ----------------
bolly = "src/Bollywood.xlsx"
histry = "src/HISTORY.xlsx"
tech = "src/Technology.xlsx"
science = "src/Science.xlsx"
sport = "src/SPORTS.xlsx"

def get_question(data,total_questions):
    new_data = data.sample(n=total_questions)
    data_shuffled = new_data.sample(frac=1) # shuffle the data set
    return data_shuffled 


def print_question(row):
    print("\n❓ Question:", row["Question"])
    print(f"A. {row['Option A']}\nB. {row['Option B']}\nC. {row['Option C']}\nD. {row['Option D']}")


def load_excel(path: str, level : int):
    if not os.path.exists(path):
        print(f"Quiz file not found: {path}")
        return None
    try:
        df = pd.read_excel(path)
        level = {
            1 : "Hard",
            2 : "Medium",
            3 : "Easy"
        }[level]
        df = df[df["Difficulty"] == level] # filter data according to level
    except Exception as e:
        print("Error loading quiz file:", e)
        return None

    required_cols = {"Question", "Option A", "Option B", "Option C", "Option D", "Answer"}
    if not required_cols.issubset(df.columns):
        print("Excel file must contain columns:", required_cols)
        return None

    df = df.dropna(subset=list(required_cols))
    if df.empty:
        print("No valid questions found in the quiz file.")
        return None
    return df


# ---------------- CHECK ANSWER ----------------
def check_answer(row, user_answer):
    correct = str(row["Answer"]).strip().upper()
    user = user_answer.strip().upper()
    if user == correct:
        print("✅ Correct!")
        return True
    else:
        option_text = row.get(f"Option {correct}", "Unknown")
        print(f"❌ Wrong! The correct answer is: {correct}. {option_text}")
        return False
    
def choose_level():
    print("choose a level : ")
    print("1. Hard\n2. Medium\n3. Easy")
    level = None
    while level not in (1,2,3):
        level = int(input("Enter 1, 2 or 3 :"))
    return level

# ---------------- QUIZ FUNCTION ----------------
def start_quiz():
    clear_ter()         # clear reg and login part 
    print_app_title()
    print(f"hi, {username} let's START YOUR QUIZ , 𝐵𝑒𝓈𝓉 𝑜𝒻 𝓁𝓊𝒸𝓀")
    print("Choose a quiz category:")
    print("1. Bollywood")
    print("2. History")
    print("3. Technology")
    print("4. Science")
    print("5. Sports")
    choice = input("Enter 1, 2, 3, 4, or 5: ").strip()

    category_name = ""  
    if choice == "1":
        level = choose_level()
        df = load_excel(bolly,level)
        category_name = "🎬 Bollywood Questions"
    elif choice == "2":
        level = choose_level()
        df = load_excel(histry,level)
        category_name = "📜 History Questions"
    elif choice == "3":
        level = choose_level()
        df = load_excel(tech,level)
        category_name = "💻 Technology Questions"
    elif choice == "4":
        level = choose_level()
        df = load_excel(science,level)
        category_name = "🔬 Science Questions"
    elif choice == "5":
        level = choose_level()
        df = load_excel(sport,level)
        category_name = "⚽ Sports Questions"
    else:
        print("Invalid choice.")
        return

    if df is None:
        return

    # ---------------- Loop until user says NO ----------------
    asked = 0
    score = 0
    start = time.time()
    while True:
        # ---------------- Choose number of questions ----------------
        while True:
            try:
                total_qs = int(input("How many questions do you want to practice (e.g., 10, 20, 30): "))
                if total_qs > 0:
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")

        print(f"\n📌 You chose to practice {total_qs} questions.\n")
        # time.sleep(1)
        qno = 0
        # ---------------- Run the quiz ----------------
        que_set = get_question(df,total_qs)
        for _ ,que in que_set.iterrows():
            clear_ter()
            print_app_title()
            print(f"Hi {username} let's start quiz")
            print(category_name)
            print(f"Question {qno+1} of {total_qs}")

            # 🔹 Show timer message before question

            # print the question
            print_question(que)

            # ⏳ timer input (10 sec)
            user_answer = input_with_timeout("Enter your answer (A/B/C/D or Q to quit): ", timeout=30)

            if user_answer is None:   # timeout
                print("❌ You missed the question.")
                print("-" * 40)
                time.sleep(1)
                asked += 1
                qno += 1
                continue

            user_answer = user_answer.strip()
            if user_answer.lower() == "q":
                print("Thank you for playing!")
                return   # exit completely

            if check_answer(que, user_answer):   # ✅ now returns True/False
                score += 1
                
            print("-" * 40)
            time.sleep(1.5)
            asked += 1
            qno += 1

        # ---------------- Final score ----------------
        print(f"\n🏆 You got {score} out of {asked} correct!\n")   # ✅ now works
    
        # ---------------- Ask play again ----------------
        play_again = input("Do you want to play again? (Y/N): ").strip().lower()
        if play_again != "y":
            print("\n👋 Thank you for playing! Goodbye!\n")
            end = time.time()
            duration = end - start # calculate spent time
            update_progrss(duration,score,asked)
            break

# ---------------- MAIN MENU ----------------
def login_page():
    while True:
        clear_ter()
        print_app_title()
        print("\n--- MENU ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose option (1/2/3): ")
        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
            return True
        elif choice == "3":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice, try again.")
            time.sleep(1)


# ---------------- MAIN MENU ----------------
def main_menu():
    # global username
    # username = "bubai"
    # print("1. Play Quiz\n2. show progress")
    # choice = input("Choose option (1/2): ")
    # if choice == 1:
    #     start_quiz()
    # else :
    #     show_progress()
    
    if login_page() :  #user go to the main page when successfully login
        while True:
            print("1. Play Quiz\n2. show progress\n3. Show Leaderboard\n4. exit")
            choice = int(input("Choose option (1,2,3 or 4): "))
            if choice == 1:
                start_quiz() 
            elif choice == 2 :
                show_progress()
            elif choice == 3 :
                show_leaderboard()
            elif choice == 4 :
                print("👋 Exiting... Goodbye!")
                break
            else :
                print("❌ invalid choice Try again")
                time.sleep(1)



# ---------------- RUN PROGRAM ----------------
if __name__ == "__main__":
    main_menu()