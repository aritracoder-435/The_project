# Simple Quize Application using Python
# 🧠 Quizy

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/aritracoder-435/The_project)](https://github.com/aritracoder-435/The_project.git/issues)

A simple *Python-based quiz application*.  
Users can answer multiple-choice questions, get instant feedback, and see their final score at the end.

Quizy Website : https://quizy-kucp.onrender.com
---

## ✨ Features

- ✅ User login & registration
- ✅ Multiple-choice questions with level 
- ✅ Each Question has a timer  
- ✅ Instant feedback on answers
- ✅ Score tracking  
- ✅ show simple progrss
- ✅ Leaderboard

---

## 🚀 Installation

1. For Terminal :
   1. Clone the repository:
      ```bash
      git clone https://github.com/aritracoder-435/The_project.git
      cd Quiz_App
   2. Run the app:
      ```bash
      python Quiz_in_Terminal.py
2. For Website :
   1. Clone the repository:
      ```bash
      git clone https://github.com/aritracoder-435/The_project.git
      cd Quiz_App
   2. Create Virtual Environment (Optional But Recomended):
      1. Create :
         ```bash
         python -m venv venv
      2. Activate :
         ```bash
         venv\Scripts\Activate
   3. Download Dependency :
      ```bash
      pip install -r requirements.txt
   4. Run App :
      ```bash
      python Quiz_in_Website.py
---
## Project Structure
1. For Terminal :
   ```
   Quiz_App/
   ├── QUIZ_APPLICATION/
   |   ├── Quiz_In_Website.py
   ├── src/
   |   ├── All Source file
   └── README.md          # Project documentation
2. For Website :
   ```
   Quiz_App/
   ├── QUIZ_APPLICATION/
   |   ├── static/
   |   |     ├── bg.png
   |   |     ├── icon.png
   |   |     ├── style.css
   |   ├── templates/
   |   |     ├── base.html
   |   |     ├── category.html
   |   |     ├── leaderboard.html
   |   |     ├── login.html
   |   |     ├── profile.html
   |   |     ├── quiz.html
   |   |     ├── registration.html
   |   |     ├── result.html
   |   ├── Quiz_In_Terminal.py
   ├── src/
   |   ├── All Source file
   └── README.md          # Project documentation
---
## Contributing
1. Fork the repository
2. Create a new branch (git checkout -b feature-name)
3. Make your changes
4. Submit a pull request