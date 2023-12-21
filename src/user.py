import json

# Json文件处理
class JsonFileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def write_json_to_file(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=2)

    def read_json_from_file(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data

import sqlite3
from datetime import datetime, timedelta

# 数据库连接
DB_FILE = 'data/chatbox.db'
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create user table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    password TEXT,
    email TEXT UNIQUE,
    role TEXT DEFAULT 'user',
    is_valid INTEGER DEFAULT 0,
    registration_ip TEXT,
    registration_date TEXT,
    expiration_date TEXT,
    current_key TEXT,
    proxy_url TEXT,
    default_model TEXT,
    avatar_link TEXT
)
''')
conn.commit()


class User:
    def __init__(self, name=None, password=None, email=None, registration_ip=None): 
        self.name = name
        self.password = password
        self.email = email
        self.role = 'user'
        self.is_valid = False
        self.registration_ip = registration_ip
        self.registration_date = None
        self.expiration_date = None
        self.current_key = None
        self.proxy_url = None
        self.default_model = "gpt-3.5-turbo"
        self.avatar_link = None

    def to_dict(self) -> dict:
        """
        Convert User instance to a dictionary.
        """
        user_dict = {
            'name': self.name,
            'password': self.password,
            'email': self.email,
            'role': self.role,
            'is_valid': self.is_valid,
            'registration_ip': self.registration_ip,
            'registration_date': self.registration_date,
            'expiration_date': self.expiration_date,
            'current_key': self.current_key,
            'proxy_url': self.proxy_url,
            'default_model': self.default_model,
            'avatar_link': self.avatar_link
        }
        return user_dict

    def __str__(self):
        return self.name
    
    def validate(self):
        # 验证数据
        if not (self.name and len(self.name) > 2):
            raise ValueError("姓名必须是长度大于2的文本")
        if not (self.password and len(self.password) >= 6 and any(c.isupper() for c in self.password)
                and any(c.islower() for c in self.password) and any(c.isdigit() for c in self.password)):
            raise ValueError("密码必须是6位以上，包括大小写字母和数字")
        if not (self.email and '@' in self.email and '.' in self.email):
            raise ValueError("邮箱必须是有效邮箱")
        if not (self.default_model and self.default_model in ("gpt-3.5-turbo","gpt-4")):
            raise ValueError("所选模型不支持")
    
    def valiemail(self):
        # 检查重复邮箱
        cursor.execute("SELECT COUNT(*) FROM user WHERE email = ?", (self.email,))
        if cursor.fetchone()[0] > 0:
            raise FileExistsError("User with the same email already exists")

    def valiname(self):
        # 检查重复用户名
        cursor.execute("SELECT COUNT(*) FROM user WHERE name = ?", (self.name,))
        if cursor.fetchone()[0] > 0:
            raise FileExistsError("User with the same name already exists")

    def save(self, update=False):
        # 保存数据
        self.validate()
        cursor.execute('''
        INSERT OR REPLACE INTO user (
            name, password, email, role, is_valid, registration_ip,
            registration_date, expiration_date, current_key, proxy_url, default_model, avatar_link
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.name, self.password, self.email, self.role, self.is_valid, self.registration_ip,
              self.registration_date, self.expiration_date, self.current_key, self.proxy_url,
              self.default_model, self.avatar_link))
        conn.commit()

    def set_user_inf(self, **kwargs):
        # 更新属性
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self, **kwargs):
        self.set_user_inf(**kwargs)
        self.save(update=True)

    @staticmethod
    def register(name: str, password: str, email: str, registration_ip: str):
        user = User(
            name=name,
            password=password,
            email=email,
            registration_ip=registration_ip
        )
        user.valiname()
        user.valiemail()
        user.registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user.expiration_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
        user.validate()
        user.save()
        return user

    @staticmethod
    def login(name: str | None = None, password: str | None = None, registration_ip: str | None = None):
        if not name or not password:
            raise ValueError("用户名/邮箱和密码是必填项")

        query = "SELECT * FROM user WHERE (name = ? or email = ?) AND password = ?"
        cursor.execute(query, (name, name, password))
        user_data = cursor.fetchone()

        if user_data:
            user = User(
                name=user_data[1],
                password=user_data[2],
                email=user_data[3],
                registration_ip=user_data[6]
            )
            user.is_valid = bool(user_data[5])
            user.role = user_data[4]
            user.registration_date = user_data[7]
            user.expiration_date = user_data[8]
            user.current_key = user_data[9]
            user.proxy_url = user_data[10]
            user.default_model = user_data[11]
            return user
        else:
            raise ValueError("验证失败，用户名/邮箱或者密码错误！")

    @staticmethod
    def query(username=None, email=None):
        if username:
            query = "SELECT * FROM user WHERE name = ?"
            cursor.execute(query, (username,))
        elif email:
            query = "SELECT * FROM user WHERE email = ?"
            cursor.execute(query, (email,))
        else:
            query = "SELECT * FROM user"
            cursor.execute(query)

        user_list = []
        for user_data in cursor.fetchall():
            user_info = {
                'name': user_data[1],
                'email': user_data[3],
                'registration_date': user_data[7],
                'is_valid': bool(user_data[5]),
                'expiration_date': user_data[8],
                'role': user_data[4]
            }
            user_list.append(user_info)

        return user_list


# 例子
# 注册新用户
# new_user = User()
# new_user.register(name="John", password="Psd123", email="john.doe@example.com", registration_ip="127.0.0.1")

# 登录用户
logged_in_user = User.login(name="John", password="Psd123")
# if logged_in_user:
#     print(f"Logged in as: {logged_in_user.name}")
# else:
#     print("Login failed")
# logged_in_user.update(registration_ip='189.169.21.23')
logged_in_user.update(current_key='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')
logged_in_user.update(proxy_url='https://chatgpt-api-proxy.cc')
print(logged_in_user)

        
# 查询用户
# all_users = User.query()
# print("All Users:")
# print(all_users)

# specific_user = User.query(username="John")
# print("Specific User:")
# print(specific_user)

# specific_user_by_email = User.query(email="john.doe@example.com")
# print("Specific User by Email:")
# print(specific_user_by_email)
