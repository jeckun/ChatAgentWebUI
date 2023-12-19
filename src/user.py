import json
import sqlite3
from datetime import datetime, timedelta

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

# 数据库连接
DB_FILE = 'data/chatbox.db'
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# 创建用户表
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
    default_model TEXT
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
        self.registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.expiration_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
        self.current_key = None
        self.proxy_url = None
        self.default_model = None

    def validate(self):
        if not (self.name and len(self.name) > 2):
            raise ValueError("姓名必须是长度大于2的文本")
        if not (self.password and len(self.password) >= 6 and any(c.isupper() for c in self.password)
                and any(c.islower() for c in self.password) and any(c.isdigit() for c in self.password)):
            raise ValueError("密码必须是6位以上，包括大小写字母和数字")
        if not (self.email and '@' in self.email and '.' in self.email):
            raise ValueError("邮箱必须是有效邮箱")

    def save(self, update=False):
        self.validate()
        if not update:
            # 检查邮箱是否已存在
            cursor.execute("SELECT COUNT(*) FROM user WHERE email = ?", (self.email,))
            if cursor.fetchone()[0] > 0:
                raise FileExistsError("同名文件已存在")

        # 存入数据库
        cursor.execute('''
        INSERT OR REPLACE INTO user (
            name, password, email, role, is_valid, registration_ip,
            registration_date, expiration_date, current_key, proxy_url, default_model
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.name, self.password, self.email, self.role, self.is_valid, self.registration_ip,
              self.registration_date, self.expiration_date, self.current_key, self.proxy_url, self.default_model))
        conn.commit()

    def register(self):
        self.validate()
        self.save()
        # 发送消息给管理员（假设管理员邮箱为 admin@example.com）
        admin_email = 'admin@example.com'
        admin_message = f"New user registered: {self.name} ({self.email})"
        cursor.execute("SELECT COUNT(*) FROM user WHERE email = ?", (admin_email,))
        if cursor.fetchone()[0] > 0:
            cursor.execute("SELECT * FROM user WHERE email = ?", (admin_email,))
            admin_data = cursor.fetchone()
            admin_data = {
                'name': admin_data[1],
                'password': admin_data[2],
                'email': admin_data[3],
                'role': admin_data[4],
                'is_valid': bool(admin_data[5]),
                'registration_ip': admin_data[6],
                'registration_date': admin_data[7],
                'expiration_date': admin_data[8],
                'current_key': admin_data[9],
                'proxy_url': admin_data[10],
                'default_model': admin_data[11]
            }
            admin_data['messages'].append(admin_message)

            # 更新管理员数据
            cursor.execute('''
            UPDATE user SET
                name=?, password=?, email=?, role=?, is_valid=?, registration_ip=?,
                registration_date=?, expiration_date=?, current_key=?, proxy_url=?, default_model=?
            WHERE email=?
            ''', (admin_data['name'], admin_data['password'], admin_data['email'], admin_data['role'],
                  int(admin_data['is_valid']), admin_data['registration_ip'], admin_data['registration_date'],
                  admin_data['expiration_date'], admin_data['current_key'], admin_data['proxy_url'],
                  admin_data['default_model'], admin_email))
            conn.commit()

    @staticmethod
    def login(username=None, email=None, password=None):
        if not (username or email) or not password:
            raise ValueError("用户名/邮箱和密码是必填项")

        query = "SELECT * FROM user WHERE name = ? OR email = ? AND password = ?"
        cursor.execute(query, (username, email, password))
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
            return None

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
# new_user = User(name="John Doe", password="Password123", email="john.doe@example.com", registration_ip="127.0.0.1")
# new_user.register()

# 登录用户
# logged_in_user = User.login(email="john.doe@example.com", password="Password123")
# if logged_in_user:
#     print(f"Logged in as: {logged_in_user.name}")
# else:
#     print("Login failed")

# 查询用户
# all_users = User.query()
# print("All Users:")
# print(all_users)

# specific_user = User.query(username="John Doe")
# print("Specific User:")
# print(specific_user)

# specific_user_by_email = User.query(email="john.doe@example.com")
# print("Specific User by Email:")
# print(specific_user_by_email)
