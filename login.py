from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2.QtCore import Qt, QUrl, QTimer
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtMultimediaWidgets import QVideoWidget
import os
from PySide2.QtWidgets import QMessageBox
import psycopg2
import hashlib
import bcrypt
from datetime import datetime
from window import MainWindow
from open_Gauss import create_conn


class Login(QtWidgets.QMainWindow):
    """ 登录UI """
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('./ui/login.ui')
        self.ui.setWindowTitle('Login')
        self.ui.setWindowIcon(QIcon('./ui/icons/icon1.png'))
        self.ui.login.clicked.connect(self.login)
        self.ui.register_2.clicked.connect(self.register)

    def login(self):
        """ 登录按钮 的连接函数，用于登录"""
        username = self.ui.username.text()
        password = self.ui.password.text()

        conn = create_conn()
        cur = conn.cursor()  # 创建光标：

        # 查询数据库中的用户信息
        cur.execute("SELECT username, password_hash FROM users WHERE username = %s;", (username,))
        user_info = cur.fetchone()

        if user_info:
            stored_password_hash = user_info[1]
            # 使用SHA-256哈希验证密码
            entered_password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

            if entered_password_hash == stored_password_hash:
                QMessageBox.information(self, "Login", "Login successfully")
                # 登录成功，打开MainWindow

                self.main_window = MainWindow()
                self.main_window.ui.show()

                self.ui.hide()  # 关闭登录窗口
            else:
                QMessageBox.warning(self, "Login", "Invalid username or password")
        else:
            QMessageBox.warning(self, "Login", "User not found")

        # 关闭连接
        cur.close()
        conn.close()

    def register(self):
        """ 注册按钮 连接函数，用于注册用户"""
        username = self.ui.username.text()
        password = self.ui.password.text()
        conn = create_conn()
        cur = conn.cursor()  # 创建光标：

        # 检查用户名是否已存在
        cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
        existing_user = cur.fetchone()

        if not existing_user:
            # 使用SHA-256哈希密码
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            # 插入用户名和密码哈希到数据库
            cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s);", (username, hashed_password))
            conn.commit()
            QMessageBox.information(self, "Registration", "Registration successful")
        else:
            QMessageBox.warning(self, "Registration", "Username already exists")

        # 关闭连接
        cur.close()
        conn.close()


if __name__ == '__main__':
    app = QApplication([])
    login = Login()
    login.ui.show()
    app.exec_()
