from flask import Flask
import src.views as views

app = Flask('ChatGPT-Bot')

app.add_url_rule('/', 'home', views.index)
app.add_url_rule('/about', 'about', views.about)
app.add_url_rule('/personal', 'personal', views.personal)
app.add_url_rule('/send_message', 'send_message', views.send_message, methods=['POST'])
app.add_url_rule('/set_key', 'set_key', views.set_openai_key, methods=['POST'])
app.add_url_rule('/clear_chat', 'clear_chat', views.clear_chat, methods=['POST'])
