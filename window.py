import cv2
from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2.QtCore import Qt, QUrl, QTimer
from detect_face import detect_face
from detect_arcface import detect_arcface
from detect_facenet import detect_facenet
import threading
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtMultimediaWidgets import QVideoWidget
import os
from open_Gauss import create_conn
from datetime import datetime


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('./ui/main_window.ui')
        self.ui.setWindowTitle('Main-Window')
        self.ui.setWindowIcon(QIcon('./ui/icons/icon2.png'))
        self.ui.button1.clicked.connect(self.open_window1)
        self.ui.button2.clicked.connect(self.open_window2)

    def open_window1(self):
        self.window1 = Window1()
        self.window1.ui1.show()
        self.hide()

    def open_window2(self):
        self.window2 = Window2()
        self.window2.ui2.show()
        self.hide()


class Window1(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui1 = QUiLoader().load('ui/window1.ui')
        self.ui1.setWindowTitle('Face-Detection')
        self.ui1.setWindowIcon(QIcon('./ui/icons/icon3.png'))
        self.ui1.start.clicked.connect(self.start_thread)
        self.ui1.stop.clicked.connect(self.stop_thread)
        self.ui1.select.clicked.connect(self.select_handle)
        self.ui1.show1.clicked.connect(self.show_handle)
        self.ui1.upload.clicked.connect(self.upload)
        self.is_running = False
        self.worker_thread = None
        self.input_filename = None
        self.output_filename = None
        self.media_player = QMediaPlayer(self)
        self.video_update = None

    def upload(self):
        conn = create_conn()
        cur = conn.cursor()  # 创建光标：

        current_time = datetime.now()
        # 读取图片文件并将二进制数据存储到数据库

        file = self.output_filename
        with open(file, 'rb') as file:
            file_data = file.read()
        attribute = None
        if self.ui1.comboBox.currentText() == '图片':
            attribute = 'image'
        elif self.ui1.comboBox.currentText() == '视频':
            attribute = 'video'
        cur.execute("INSERT INTO icons (attribute, timestamp, content) VALUES (%s, %s, %s);",
                    (attribute, current_time, file_data))
        conn.commit()

        # 关闭连接
        cur.close()
        conn.close()

        # 弹出消息框
        QMessageBox.information(self, "Success", "Data inserted successfully")

    def select_handle(self):
        # button-select连接函数
        self.video_update = False
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.input_filename, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                             "All Files (*.png *.jpg *.bmp *.mp4)",
                                                             options=options)
        if self.input_filename:
            if self.input_filename.endswith(('.png', '.jpg', '.bmp')):
                pixmap = QPixmap(self.input_filename)
                label_size = self.ui1.input.size()
                scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.ui1.input.setPixmap(scaled_pixmap)
            elif self.input_filename.endswith(('.mp4')):
                self.cap = cv2.VideoCapture(self.input_filename)
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update_frame)
                self.timer.start(30)  # 30 milliseconds interval

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            label_size = self.ui1.input.size()
            scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if not self.video_update:
                self.ui1.input.setPixmap(scaled_pixmap)
            if self.video_update:
                self.ui1.output.setPixmap(scaled_pixmap)
        else:
            self.cap.release()
            self.timer.stop()  # 停止定时器

    def show_handle(self):
        self.video_update = True
        self.output_filename = self.input_filename.replace('input', 'output')
        print(self.output_filename)
        if self.output_filename:
            if self.output_filename.endswith(('.png', '.jpg', '.bmp')):
                pixmap = QPixmap(self.output_filename)
                label_size = self.ui1.output.size()
                scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.ui1.output.setPixmap(scaled_pixmap)
            elif self.output_filename.endswith(('.mp4')):
                self.cap = cv2.VideoCapture(self.output_filename)
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update_frame)
                self.timer.start(30)  # 30 milliseconds interval

    def start_thread(self):
        # if not self.is_running:
        self.is_running = True
        self.worker_thread = threading.Thread(target=self.start_handle)
        self.worker_thread.start()

    def start_handle(self):
        # button1的连接函数
        choice = self.ui1.comboBox.currentText()
        if choice == '摄像头':
            self.ui1.input.clear()
            self.ui1.output.clear()
            choice = 0
        if choice == '图片' or choice == '视频':
            choice = self.input_filename

        detect_face(choice)

    def stop_handle(self):

        # self.is_running = False
        self.cap.release()
        cv2.destroyAllWindows()

    def stop_thread(self):
        self.worker_thread_stop = threading.Thread(target=self.stop_handle)
        self.worker_thread_stop.start()


class Window2(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui2 = QUiLoader().load('ui/window2.ui')
        self.ui2.setWindowTitle('Face-Recognition')
        self.ui2.setWindowIcon(QIcon('./ui/icons/icon4.png'))
        self.ui2.start.clicked.connect(self.start_thread)
        self.ui2.stop.clicked.connect(self.stop_thread)
        self.ui2.select.clicked.connect(self.select_handle)
        self.ui2.show2.clicked.connect(self.show_handle)
        self.ui2.upload.clicked.connect(self.upload)
        self.output_filename = None
        self.is_running = False
        self.worker_thread = None
        self.input_filename = None
        self.output_filename = None
        self.media_player = QMediaPlayer(self)
        self.video_update = None
        self.cap = None

    def upload(self):
        conn = create_conn()
        cur = conn.cursor()  # 创建光标：

        current_time = datetime.now()
        # 读取图片文件并将二进制数据存储到数据库

        file = self.output_filename
        with open(file, 'rb') as file:
            file_data = file.read()
        attribute = None
        if self.ui2.comboBox_2.currentText() == '图片':
            attribute = 'image'
        elif self.ui2.comboBox_2.currentText() == '视频':
            attribute = 'video'
        cur.execute("INSERT INTO icons (attribute, timestamp, content) VALUES (%s, %s, %s);",
                    (attribute, current_time, file_data))
        conn.commit()

        # 关闭连接
        cur.close()
        conn.close()

        # 弹出消息框
        QMessageBox.information(self, "Success", "Data inserted successfully")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            label_size = self.ui2.input.size()
            scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if not self.video_update:
                self.ui2.input.setPixmap(scaled_pixmap)
            if self.video_update:
                self.ui2.output.setPixmap(scaled_pixmap)
        else:
            self.cap.release()
            self.timer.stop()  # 停止定时器

    def select_handle(self):
        # button-select连接函数
        self.video_update = False
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.input_filename, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                             "All Files (*.png *.jpg *.bmp *.mp4)",
                                                             options=options)
        if self.input_filename:
            if self.input_filename.endswith(('.png', '.jpg', '.bmp')):
                pixmap = QPixmap(self.input_filename)
                label_size = self.ui2.input.size()
                scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.ui2.input.setPixmap(scaled_pixmap)
            elif self.input_filename.endswith(('.mp4')):
                self.cap = cv2.VideoCapture(self.input_filename)
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update_frame)
                self.timer.start(30)  # 30 milliseconds interval

    def show_handle(self):
        self.video_update = True
        self.output_filename = self.input_filename.replace('input', 'output')
        print(self.output_filename)
        if self.output_filename:
            if self.output_filename.endswith(('.png', '.jpg', '.bmp')):
                pixmap = QPixmap(self.output_filename)
                label_size = self.ui2.output.size()
                scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.ui2.output.setPixmap(scaled_pixmap)
            elif self.output_filename.endswith(('.mp4')):
                self.cap = cv2.VideoCapture(self.output_filename)
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update_frame)
                self.timer.start(30)  # 30 milliseconds interval

    def start_handle(self):
        # button-start的连接函数
        choice_1 = self.ui2.comboBox_1.currentText()
        choice_2 = self.ui2.comboBox_2.currentText()
        if choice_1 == 'arcface':
            if choice_2 == '摄像头':
                self.ui2.input.clear()
                self.ui2.output.clear()
                choice_2 = 0
            else:
                choice_2 = self.input_filename
            detect_arcface(choice_2)

        if choice_1 == 'facenet':
            if choice_2 == '摄像头':
                self.ui2.input.clear()
                self.ui2.output.clear()
                choice_2 = 0
            else:
                choice_2 = self.input_filename
            detect_facenet(choice_2)
            self.cap.release()

    def start_thread(self):
        if not self.is_running:
            self.worker_thread = threading.Thread(target=self.start_handle)
            self.worker_thread.start()

    def stop_handle(self):

        # self.is_running = False
        self.cap.release()
        cv2.destroyAllWindows()

    def stop_thread(self):
        self.worker_thread_stop = threading.Thread(target=self.stop_handle)
        self.worker_thread_stop.start()


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.ui.show()
    app.exec_()
