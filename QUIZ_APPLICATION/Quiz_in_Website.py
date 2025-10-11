from flask import Flask,flash,render_template,request,redirect,url_for,session
import pandas as pd
import os, json,time,math

#load user
def load_users():
    if os.path.exists("src/dataBase.json"):
        with open("src/dataBase.json", "r") as f:
            return json.load(f)
    else:
        print('no database')
# save user new data
def save_users(users):
    with open("src/dataBase.json", "w") as f:
        json.dump(users, f, indent=4)

# load questions data set
def load_questions(path):
    df = pd.read_excel(path)
    if df.empty:
            return None
    return df

# get question data set according to total questions number
def get_question(data,total_questions):
    new_data = data.sample(n=total_questions)
    data_shuffled = new_data.sample(frac=1).reset_index(drop = True) # shuffle the data set with reseting index
    return data_shuffled 

# password requirment check
def set_password(min_length,pwd):
    has_upper = has_lower = has_digit = has_special = False
    has_space = " " in pwd   #  check for space
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

    if pass_length and has_upper and has_lower and has_digit and has_special and (not has_space):
        return True   # return True when password is correct
    else:
        flash("❌ Password is NOT valid.")
        flash("   📌 Password must contain:")
        if not pass_length:
            flash("    - At least 8 characters")
        if not has_upper:
            flash("    - At least one uppercase letter")
        if not has_lower:
            flash("    - At least one lowercase letter")
        if not has_digit:
            flash("    - At least one digit")
        if not has_special:
            flash("    - At least one special character (!@#$ etc.)")
        if has_space:
            flash("    - No spaces allowed in the password")
        flash("⚠ Please try again.")
        return False

def update_progrss(duration,score,asked,username):
    data = load_users()
    sub = data["users_data"][username]["progress"]
    sub["score"] += score
    sub["time_spent"] += duration
    sub["attempt"] += asked

    save_users(data)

# application
app = Flask(__name__)

app.secret_key = 'my_secret' # for using session

@app.route('/')
def home ():
    if 'user' in session :
        return render_template('base.html', 
                               user = session['user'] if 'user' in session else ' ',
                               active_page = 'home')
    return redirect(url_for('login'))

# user Registration
@app.route("/registration",methods = ["GET","POST"])
def registration():
    if request.method == "POST" :
        data = load_users()
        users = data["users_data"]
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users :
            flash("Username already exist try again")
            return redirect(url_for("registration"))
        elif set_password(5,password) :
            flash("Registration successfully! now Login")
            # Add new user with progress
            data["users_data"][username] = {
            "password": password,
            "progress": {
                "time_spent":0,
                "score": 0,
                "attempt":0
            }
            }
            save_users(data)
            return redirect(url_for('login'))
    return render_template("registration.html", active_page = 'home')

#entering quiz page via login then category
@app.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "POST" :
        data = load_users()
        users = data["users_data"]
        username = request.form.get("username")
        password = request.form.get('password')
        if (username in users) and (password == users[username]['password']) :
            flash("Logged in successfully!")
            session['user'] = username
            return redirect(url_for('start'))
        else :
            flash("Invalid password or username")
            return redirect(url_for('login'))

    return render_template("login.html",active_page = 'home')

#quiz start route
@app.route('/start' ,methods = ["GET" , "POST"]) 
def start():
    if 'user' in session :
        if request.method == 'POST' :
            category = request.form.get('category')
            total_question = int(request.form.get('question_no'))
            category = {
                'a' :"src/Bollywood.xlsx",
                'b'  :"src/HISTORY.xlsx",
                'c' : "src/SCIENCE.xlsx",
                'd' : "src/SPORTS.xlsx",
                'e' : "src/Technology.xlsx"
                }[category]
            
            df = load_questions(category)
            global questions 
            questions = get_question(df,total_question)
            session['start_time'] = time.time()
            session["q_no"] = 0
            session['user_ans'] = [None] * total_question
            session["total_q"] = total_question
            session['iteams'] = []
            for _, q in questions.iterrows() :
                session['iteams'].append({
                    'question' : q["Question"],
                    'options' :[q["Option A"], 
                                q["Option B"],
                                q["Option C"],
                                q["Option D"]],
                    'answer' :  (q["Answer"].upper(), 
                                {'a' :q["Option A"], 
                                'b' : q["Option B"],
                                'c' :q["Option C"],
                                'd' :q["Option D"]}[q["Answer"].lower()]
                                )
                    })
            return redirect(url_for('quiz'))
        return render_template('category.html',
                               user = session['user'] if 'user' in session else ' ',
                               active_page = 'quiz') #choose quiz question category
    else :
        flash("Login to play quiz")
        return redirect(url_for('login'))

# main quiz route
@app.route('/quiz', methods = ["GET" , "POST"]) 
def quiz():
    now = time.time()
    remaining = (60 * session['total_q'])-int((now - session['start_time']))
    current = session.get('q_no')
    total_question = session.get('total_q')

    remaining = int(remaining) if remaining % 1 <= 0.5 else math.ceil(remaining)

    if request.method == 'POST' :
        ans = str(request.form.get('answer'))
        session['user_ans'][current] = ans.split('#')
        if 'next' in request.form :
            current += 1
        elif 'prev' in request.form :
            current -= 1
        else:
            pass
        if (current >=  total_question) or (remaining <= 0):
            session['end'] = time.time()
            score = 0
            for i ,ans in enumerate(session['user_ans']) :
                print(session['user_ans'])
                if str(ans[1]if ans not in (['None'], None) else ' ').lower() == str(session['iteams'][i]['answer'][1]).lower() :
                    score += 1
            session['score'] = score
            session.modified = True
            update_progrss((session['end'] - session['start_time']), score, session['total_q'], session['user'])
            return redirect(url_for('result'))
        session['q_no'] = current
    return render_template(
        "quiz.html",
        active_page = 'quiz',
        user = session['user'] if 'user' in session else ' ',
        question=session['iteams'][current]['question'],
        op1=session['iteams'][current]['options'][0],
        op2=session['iteams'][current]['options'][1],
        op3=session['iteams'][current]['options'][2],
        op4=session['iteams'][current]['options'][3],
        remaining = remaining,
        q_no = current,
        total_q = total_question,
        u_answer = session['user_ans'][current][-1] if session['user_ans'][current] is not None else "None"
        )

# after completing quiz we show result route
@app.route('/result' , methods = ["GET" , "POST"]) 
def result():
    if request.method == 'POST' :
        return redirect(url_for('start'))
    return render_template(
        'result.html',
        active_page = 'quiz',
        user = session['user'] if 'user' in session else ' ',
        questions = session['iteams'],
        u_ans = session['user_ans'],
        score = session['score'],
        total_q = session['total_q'],
        time_take =int(session['end'] - session['start_time'])-1
        )

@app.route('/leaderboard')
def leaderboadr():
    data = load_users()
    users = data["users_data"]
    if not users :
        return
    sorted_users = sorted(users.items(),key = lambda x : x[1]["progress"]["score"],reverse=True)

    return render_template('leaderboard.html',
                           active_page = 'leaderboard',
                           user = session['user'] if 'user' in session else False,
                           sorted_users = sorted_users)

@app.route('/profile')
def profile():
    if 'user' in session :
        data = load_users()
        user_p = data["users_data"][session['user']]['progress']
        secound = user_p["time_spent"]
        h = int(secound // 3600)
        m = int((secound % 3600) // 60)
        s = int((secound % 60))
        return render_template('profile.html',
                               active_page = 'profile',
                               user = session['user'] if 'user' in session else ' ',
                               time = [h,m,s] ,
                               score =user_p['score'] ,
                               asked =user_p['attempt'] )
    else :
        flash("Login to see your profile")
        return redirect(url_for('login'))

@app.route('/log_out')
def log_out():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__" :
    app.run(debug = True)