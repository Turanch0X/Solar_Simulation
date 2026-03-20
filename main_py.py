from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import math, os

app = QApplication([])
path_to_img = "images\\Planets\\Sun.ico"
main_pixmap = QPixmap(path_to_img)

class Eye(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Solar System Animation")
        # self.showFullScreen()

        self.filenames = os.listdir("images\\Planets\\")
        self.paths = [os.path.join("images\\Planets\\", filename) for filename in self.filenames]
        self.path_list = sorted(self.paths, key=os.path.getctime)
        self.path_list.pop()

        self.central_Widget = QWidget(self)
        self.central_Widget.setStyleSheet("background: grey;")
        self.setCentralWidget(self.central_Widget)

        self.big_eye = QLabel(self.central_Widget)
        self.big_eye.setPixmap(main_pixmap)
        self.big_eye.setScaledContents(True)
        self.big_eye.setGeometry(800, 350, 300, 300)
        self.big_eye.show()

        self.orbit_data = { #size, speed, radius, angle
            0: [5, 0.10, 10, 0],
            1: [15, 0.09, 30, 0],
            2: [20, 0.07, 60, 0],
            3: [8, 0.08, 80, 0],
            4: [72, 0.04, 140, 0],
            5: [54, 0.03, 200, 0],
            6: [41, 0.02, 250, 0],
            7: [30, 0.01, 320, 0]
        }

        self.planets = []

        for i in self.path_list:
            label = QLabel(self.central_Widget)
            pixmap = QPixmap(i)
            label.setPixmap(pixmap)
            label.setScaledContents(True)
            label.show()
            
            self.planets.append(label)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_orbit)
        self.timer.start(48)  # ~60 FPS


    def animate_orbit(self):
        center_x = self.big_eye.x() + self.big_eye.width() // 2
        center_y = self.big_eye.y() + self.big_eye.height() // 2
        sun_radius = self.big_eye.width() // 2
        count = len(self.planets)

        for i , eye in enumerate(self.planets):
            size, speed, radius, angle = self.orbit_data[i]

            eye.setFixedSize(size, size)
            angle += speed
            self.orbit_data[i][3] = angle

            offset = (2 * math.pi / count) * i  # spread evenly

            orbit_radius = sun_radius + radius

            x = center_x + orbit_radius * math.cos(angle + offset)
            y = center_y + orbit_radius * math.sin(angle + offset)

            x -= eye.width() // 2
            y -= eye.height() // 2

            eye.move(int(x), int(y))


ex = Eye()
ex.show()
app.exec()