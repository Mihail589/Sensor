import sys
import asyncio
import re
import os
import logging
import threading
import time
from PyQt5.QtGui import * # type: ignore
from PyQt5.QtCore import *# type: ignore
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo# type: ignore
from PyQt5.QtWidgets import *# type: ignore
import serial# type: ignore
import ui
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command
from aiogram import Router
from qasync import QEventLoop, asyncSlot# type: ignore
import bot



t1min = 10
t2min = 10
t3min = 10

t1max = 30
t2max = 30
t3max = 30
logging.basicConfig(filename="log.log", level=logging.ERROR)
class Example(QMainWindow, ui.Ui_MainWindow):# type: ignore
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loop = asyncio.new_event_loop()
        self.flag = False
        self.ser = None
        self.serialPort = None
        self.comboBox.addItems([serialPort.portName() for serialPort in QSerialPortInfo().availablePorts()])
        self.startstop.clicked.connect(self.start_serial_port)

        self.spinBox.setValue(10)
        self.spinBox_2.setValue(10)
        self.spinBox_3.setValue(10)
        self.spinBox_6.setValue(30)
        self.spinBox_4.setValue(30)
        self.spinBox_5.setValue(30)
        ####self.label = QLabel(self)

        self.pixmap1 = QPixmap(f'gray.png')
        self.pixmap2 = QPixmap(f'red.png')
        self.pixmap3 = QPixmap(f'green.png')
        self.images = [self.image, self.image_2, self.image_3, self.image_4, self.image_5, self.image_6, self.image_7]
        for i in self.images:
            i.setPixmap(self.pixmap1)


        self.pushButton.clicked.connect(self.saveData)
        self.pushButton.setEnabled(False)
        self.pushButton_2.clicked.connect(self.editMode)
        line = [self.lineEdit_9, self.lineEdit_10, self.lineEdit_11, self.lineEdit_12, self.lineEdit_13, self.lineEdit_14, self.lineEdit_15]
        with open('data.txt', "r", encoding="utf-8") as file:
            data = file.readlines()
            self.lineEdit_9.setText(data[0].rstrip('\n'))
            self.lineEdit_10.setText(data[1].rstrip('\n'))
            self.lineEdit_11.setText(data[2].rstrip('\n'))
            self.lineEdit_12.setText(data[3].rstrip('\n'))
            self.lineEdit_13.setText(data[4].rstrip('\n'))
            self.lineEdit_14.setText(data[5].rstrip('\n'))
            self.lineEdit_15.setText(data[6].rstrip('\n'))
            for i in range(7):
                if line[i].text() != "":
                    self.images[i].setPixmap(self.pixmap3)


    def editMode(self):
        self.is_editing = True
        self.indicators_active = False
        self.pushButton_2.setEnabled(True)
        self.lineEdit_9.setEnabled(True)
        self.lineEdit_10.setEnabled(True)
        self.lineEdit_12.setEnabled(True)
        self.lineEdit_11.setEnabled(True)
        self.lineEdit_14.setEnabled(True)
        self.lineEdit_13.setEnabled(True)
        self.lineEdit_15.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.pushButton.setEnabled(True)

    def saveData(self):
        if True:
            #data = [field.text() for field in self.inputFields]
            try:
                with open('data.txt', 'w', encoding='utf-8') as file:
                    #for item in data:
                    file.write(self.lineEdit_9.text() + '\n')
                    file.write(self.lineEdit_10.text() + '\n')
                    file.write(self.lineEdit_11.text() + '\n')
                    file.write(self.lineEdit_12.text() + '\n')
                    file.write(self.lineEdit_13.text() + '\n')
                    file.write(self.lineEdit_14.text() + '\n')
                    file.write(self.lineEdit_15.text() + '\n')


                #QMessageBox.information(self, 'Успех', 'Данные успешно сохранены!')
               # self.updateIndicators()
                self.indicators_active = True
            except Exception as e:
               # QMessageBox.warning(self, 'Ошибка', f'Ошибка сохранения: {e}')
               print(e)

            self.is_editing = False
            #self.pushButton.setEnabled(False)

            #self.pushButton.setEnabled(False)

            self.is_editing = False
            self.indicators_active = True
            self.pushButton_2.setEnabled(False)
            self.lineEdit_9.setEnabled(False)
            self.lineEdit_10.setEnabled(False)
            self.lineEdit_12.setEnabled(False)
            self.lineEdit_11.setEnabled(False)
            self.lineEdit_14.setEnabled(False)
            self.lineEdit_13.setEnabled(False)
            self.lineEdit_15.setEnabled(False)
            self.pushButton_2.setEnabled(True)
            self.pushButton.setEnabled(False)

        else:
            #QMessageBox.warning(self, 'Ошибка', 'Сначала нажмите кнопку "Редактировать"')
            print("Ошибка")

    @asyncSlot()
    async def start_serial_port(self):
        """Запуск асинхронной задачи для работы с последовательным портом."""
        port_name = self.comboBox.currentText()
        period = self.comboBox_2.currentText() # период отправки сообщений в телеграм
        if port_name:
            if self.flag == False:
                self.startstop.setText("СТОП")
                #user_id = self.textbox.text('lineEdit_7')
                user_id = self.lineEdit_7.text() # chat id пользователя телеграмм
                self.repaint()
                self.flag = True
                self.timer = QTimer()
                self.timer.timeout.connect(self.logData)  # Подключаем обработчик
                self.timer.start(15000)  # Запускаем таймер (1000 мс = 1 сек)
                await self.open_serial_port(port_name)

            else:
                self.startstop.setText("СТАРТ")
                self.timer.stop()  # Остановка таймера
                self.repaint()
                self.flag = False
                self.ser.close()

        else:
            pass
            #QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите порт.")# type: ignore

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
                #QMessageBox.warning(self, 'Ошибка', f'Файл data.txt не найден')
                pass
        except Exception as e:
            #QMessageBox.warning(self, 'Ошибка', f'Ошибка загрузки: {e}')
            print(e)
    async def open_serial_port(self, port_name):
        """Асинхронное чтение данных из последовательного порта."""
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self.read_from_port, port_name)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть порт: {e}")# type: ignore
    def read_from_port(self, port_name):
        """Синхронное чтение данных из последовательного порта (выполняется в потоке)."""
        try:
            self.ser = serial.Serial(port_name, baudrate=9600, timeout=1)
            print(f"Порт {port_name} успешно открыт.")
            
            while True:
                line = self.ser.readline()
                if line:
                    data = re.split(r"[,']", line.decode('utf-8').strip())
                    print(data)
                    self.lineEdit.setText(data[0])
                    self.lineEdit_3.setText(data[5])
                    self.lineEdit_4.setText(data[1])

                    self.lineEdit_5.setText(data[4])
                    self.lineEdit_6.setText(data[2])
                    self.lineEdit_8.setText(data[3])

                    t1min = self.spinBox.value()
                    t2min = self.spinBox_2.value()
                    t3min = self.spinBox_3.value()

                    t1max = self.spinBox_6.value()
                    t2max = self.spinBox_4.value()
                    t3max = self.spinBox_5.value()
                    a = 6
          #          self.lineEdit_9.setEnabled(False)
          #  self.lineEdit_10.setEnabled(False)
          #  self.lineEdit_12.setEnabled(False)
          #  self.lineEdit_11.setEnabled(False)
          #  self.lineEdit_14.setEnabled(False)
          #  self.lineEdit_13.setEnabled(False)
          #  self.lineEdit_15.setEnabled(False)
                    m = [self.lineEdit_12, self.lineEdit_12, self.lineEdit_12, self.lineEdit_12, self.lineEdit_12, self.lineEdit_9, self.lineEdit_10, self.lineEdit_12, self.lineEdit_11, self.lineEdit_14, self.lineEdit_13, self.lineEdit_15]
                    for i in self.images:
                       # print(data[a])
                        if data[a] == '1':
                            i.setPixmap(self.pixmap2)
                            data_message = f"Сработал датчик на порту по названием {m[a].text()}"
                            asyncio.create_task(bot.send_message(data_message, self.lineEdit_7.text()))
                            print(f"1 on {a}")
                        else:
                            i.setPixmap(self.pixmap3)
                        a += 1
        except Exception as e:
            print(f"Ошибка при работе с портом: {e}")

    def logData(self):
            data_message = (
                f"Показания:\n 🌫Уровень СО2 = {self.lineEdit_6.text()},\n"
                f" ☀️Освещённость = {self.lineEdit_8.text()}%,\n"
                f" 🌧Влажность = {self.lineEdit_5.text()}%,\n"
                f" 🌡Температура верхней зоны = {self.lineEdit.text()}°C,\n"
                f" 🌡Температура средней зоны = {self.lineEdit_3.text()}°C,\n"
                f" 🌡Температура нижней зоны = {self.lineEdit_4.text()}°C"
            )
            print(data_message)
            print(self.lineEdit_7.text())
            #asyncio.run_coroutine_threadsafe(bot.send_message(data_message, self.lineEdit_7.text()), self.loop)
            asyncio.create_task(bot.send_message(data_message, self.lineEdit_7.text()))
            #await (bot.send_message(data_message, int(self.lineEdit_7.text())))




if __name__ == '__main__':
    app = QApplication(sys.argv)# type: ignore

    # Использование qasync для интеграции событийного цикла
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    form = Example()
    form.show()

    with loop:
        loop.run_forever()
