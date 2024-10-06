# Cognoscente

## Description

Coming Soon!

## Installation

1) Open Terminal and Clone Repository:

```bash
git clone https://github.com/AmerikanischerAdler/cognoscente
```

2) Install Python:

If python3 is not installed on your machine, run:

**MacOS:**

```bash
brew update 
brew install python3
``` 

**TIP**: For MacOS, be sure that homebrew is installed on your machine. If not, visit https://brew.sh to install.

**Ubuntu:**

```bash
sudo apt update 
sudo apt install python3
```

3) Set Up Virtual Environment:

```bash
pip3 install virtualenv
python3 -m venv env
source env/bin/activate
```

4) Install Dependencies:

```bash
pip install -r requirements.txt
```

5) Terminate Virtual Environment:

```bash 
deactivate
```

6) Set Up MYSQL Environment Variable:

Once you have created your MYSQL account, run this command in the terminal, substituting your own password for "my_password":

```bash
echo 'export MYSQLPW="my_password"' >> ~/.bashrc
```

Do the same to set up your own secret key, substituting its value for "my_secret_key":

```bash
echo 'export SECRET_KEY="my_secret_key"' >> ~/.bashrc
```

**TIP**: This implies that you are using bash as your current shell. If not, run
the command, substituting your own shell config file for ".bashrc"

7) Create MYSQL Database and Tables:

Once you are logged into your MYSQL environment, run the following commands:

*Create Cognoscente Database:*

```mysql
CREATE DATABASE Cognoscente;
```

*Create Users Table:*

```mysql
USE Cognoscente;
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR(255), 
    email VARCHAR(255), 
    username VARCHAR(255), 
    password VARCHAR(255),
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

*Create Courses Table:*

```mysql
USE Cognoscente;
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    short_desc VARCHAR(100) NOT NULL,
    full_desc TEXT NOT NULL,
    course_type VARCHAR(100) NOT NULL,
    skill_level VARCHAR(100) NOT NULL,
    thumbnail LONGBLOB,
    image_mime_type VARCHAR(50),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creator INT NOT NULL,
    FOREIGN KEY (creator) REFERENCES users(user_id) ON DELETE CASCADE
);
```

*Create Lessons Table:*

```mysql
USE Cognoscente;
CREATE TABLE lessons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    short_desc VARCHAR(200) NOT NULL,
    thumbnail LONGBLOB,
    image_mime_type VARCHAR(50),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creator INT NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (creator) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);
```

*Create Bookmarks Table:*

```mysql
USE Cognoscente;
CREATE TABLE bookmarks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creator INT NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (creator) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);
```

## Usage

1) Open Terminal

2) Navigate to cognoscente Directory:

```bash
cd cognoscente
```

3) Start Virtual Environment

```bash
python3 -m venv env
source env/bin/activate
```

**TIP**: To terminate your virtual environment, run:

```bash
deactivate
```

4) Start Flask App:

*This will spin up a local backend server*

```bash
python3 app.py
```

**TIP**: To terminate your local server, press CTRL-C

4) Open Web Browser to New Tab or Window

5) Enter Server Address in Search Bar:

You may be able to simply click this link: http://127.0.0.1:5000/

## Inspiration

Coming Soon!
 
