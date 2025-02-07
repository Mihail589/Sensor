import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_editing = False
        self.indicators_active = False
        self.editData()

        # Таймер для записи данных каждые 5 секунд
        self.data_timer = QTimer(self)
        self.data_timer.timeout.connect(self.logData)
        self.data_timer.setInterval(5000)  # Установим интервал в 5 секунд

        # Создание фигуры для графика
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout().addWidget(self.canvas)

        # Инициализация данных для графика
        self.chart_data = {
            'CO2': [],
            'Light': [],
            'Humidity': [],
            'Temp1': [],
            'Temp2': [],
            'Temp3': []
        }



    def initUI(self):
        self.setWindowTitle('Test')
        layout = QVBoxLayout()

        self.labels = [QLabel(f'Поле {i + 1}:') for i in range(7)]
        self.inputFields = [QLineEdit(self) for _ in range(7)]
        self.indicators = [QLabel(self) for _ in range(7)]

        self.gray_pixmap = QPixmap('gray.png').scaled(15, 15)
        self.green_pixmap = QPixmap('green.png').scaled(15, 15)
        self.red_pixmap = QPixmap('red.png').scaled(15, 15)

        for label, field, indicator in zip(self.labels, self.inputFields, self.indicators):
            hbox = QHBoxLayout()
            hbox.addWidget(indicator)
            hbox.addWidget(label)
            hbox.addWidget(field)
            layout.addLayout(hbox)
            field.setEnabled(False)
            indicator.setPixmap(self.gray_pixmap)

        self.saveButton = QPushButton('Сохранить', self)
        self.saveButton.clicked.connect(self.saveData)
        self.saveButton.setEnabled(False)

        self.editButton = QPushButton('Редактировать', self)
        self.editButton.clicked.connect(self.editMode)

        # Кнопки "Старт" и "Стоп"
        self.startButton = QPushButton('Старт', self)
        self.startButton.clicked.connect(self.startLogging)

        self.stopButton = QPushButton('Стоп', self)
        self.stopButton.clicked.connect(self.stopLogging)

        layout.addWidget(self.saveButton)
        layout.addWidget(self.editButton)
        layout.addWidget(self.startButton)
        layout.addWidget(self.stopButton)
        self.setLayout(layout)

    def startLogging(self):
        if not self.data_timer.isActive():
            self.data_timer.start()
            QMessageBox.information(self, 'Старт', 'Запись данных начата!')

    def stopLogging(self):
        if self.data_timer.isActive():
            self.data_timer.stop()
            QMessageBox.information(self, 'Стоп', 'Запись данных остановлена!')

    def editMode(self):
        self.is_editing = True
        self.indicators_active = False
        self.saveButton.setEnabled(True)
        for field in self.inputFields:
            field.setEnabled(True)

    def saveData(self):
        if self.is_editing:
            data = [field.text() for field in self.inputFields]
            try:
                with open('../../../../Рабочий стол/data.txt', 'w', encoding='utf-8') as file:
                    for item in data:
                        file.write(item + '\n')
                QMessageBox.information(self, 'Успех', 'Данные успешно сохранены!')
                self.updateIndicators()
                self.indicators_active = True
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Ошибка сохранения: {e}')

            self.is_editing = False
            self.saveButton.setEnabled(False)
            for field in self.inputFields:
                field.setEnabled(False)

        else:
            QMessageBox.warning(self, 'Ошибка', 'Сначала нажмите кнопку "Редактировать"')

    def editData(self):
        try:
            if os.path.exists('data.txt'):
                with open('../../../../Рабочий стол/data.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        if i < len(self.inputFields):
                            self.inputFields[i].setText(line.strip())
                            if line.strip():  # Проверяем на пустоту
                                self.indicators[i].setPixmap(self.green_pixmap)
                            else:
                                self.indicators[i].setPixmap(self.gray_pixmap)

            else:
                QMessageBox.warning(self, 'Ошибка', f'Файл data.txt не найден')
                for indicator in self.indicators:
                    indicator.setPixmap(self.gray_pixmap)

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка загрузки: {e}')
            for indicator in self.indicators:
                indicator.setPixmap(self.gray_pixmap)

    def updateIndicators(self):
        for i, field in enumerate(self.inputFields):
            if field.text():
                self.indicators[i].setPixmap(self.green_pixmap)
            else:
                self.indicators[i].setPixmap(self.gray_pixmap)

    def updateIndicatorsFromArduino(self, arduino_data):
        if not self.indicators_active:  # Проверяем, активны ли индикаторы
            return

        states = list(map(int, arduino_data.split(',')))  # Преобразуем строку в список целых чисел

        for i, state in enumerate(states):
            if self.inputFields[i].text():  # Проверяем, введено ли значение в поле
                if state == 1:  # Если контакт замкнулся (1)
                    self.indicators[i].setPixmap(self.red_pixmap)
                else:  # Если контакт незамкнут (0)
                    self.indicators[i].setPixmap(self.green_pixmap)
            else:
                self.indicators[i].setPixmap(self.gray_pixmap)  # Если поле пустое, устанавливаем серый индикатор

    def logData(self):
        co2 = random.randint(300, 700)
        light = random.randint(0, 100)
        humidity = random.randint(0, 100)
        temp1 = random.randint(5, 30)
        temp2 = random.randint(5, 30)
        temp3 = random.randint(5, 30)

        # Генерация состояния датчиков (вместо реальных данных от Arduino)
        states = [random.randint(0, 1) for _ in range(len(self.inputFields))]
        data_string = ','.join(map(str, states))

        # Запись данных в файл
        try:
            with open('../../../../Рабочий стол/sensor_data.txt', 'a', encoding='utf-8') as file:
                # Объединяем данные в одну строку и записываем
                file.write(f'{co2},{light},{humidity},{temp1},{temp2},{temp3},{data_string}\n')
            print(f'Записаны данные: {co2},{light},{humidity},{temp1},{temp2},{temp3}, {data_string}')  # Для отладки

            # Обновляем индикаторы на основе сгенерированных данных
            self.updateIndicatorsFromArduino(data_string)

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка записи данных: {e}')

        # Обновляем данные для графика
        self.chart_data['CO2'].append(co2)
        self.chart_data['Light'].append(light)
        self.chart_data['Humidity'].append(humidity)
        self.chart_data['Temp1'].append(temp1)
        self.chart_data['Temp2'].append(temp2)
        self.chart_data['Temp3'].append(temp3)

        # Обновляем график
        self.updateChart()

    def updateChart(self):
        self.figure.clear()  # Очищаем предыдущий график
        ax = self.figure.add_subplot(111)

        # Отображаем данные
        ax.plot(self.chart_data['CO2'], label='Уровень CO2', color='blue')
        ax.plot(self.chart_data['Light'], label='Освещённость %', color='orange')
        ax.plot(self.chart_data['Humidity'], label='Влажность %', color='green')
        ax.plot(self.chart_data['Temp1'], label='Temp1', color='red')
        ax.plot(self.chart_data['Temp2'], label='Temp2', color='purple')
        ax.plot(self.chart_data['Temp3'], label='Temp3', color='cyan')

        ax.set_title('Показание с датчиков за всё время')
        ax.set_xlabel('Время (5 секунд)')
        ax.set_ylabel('Значение')
        ax.legend()
        ax.grid(True)

        self.canvas.draw()  # Обновляем отображение графика


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.resize(450, 400)
    ex.show()
    sys.exit(app.exec_())
