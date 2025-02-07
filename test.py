from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

class TimerExample(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Время: 0", self)
        self.counter = 0

        # Создаем таймер
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_label)  # Подключаем обработчик
        self.timer.start(1000)  # Запускаем таймер (1000 мс = 1 сек)

        # Оформляем интерфейс
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_label(self):
        """Обновляем текст каждую секунду"""
        self.counter += 1
        self.label.setText(f"Время: {self.counter}")

app = QApplication([])
window = TimerExample()
window.show()
app.exec()
