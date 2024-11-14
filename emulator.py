import sys
import argparse
import zipfile
import os
import platform
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt

class ShellEmulator(QWidget):
    def __init__(self, zip_path, log_path):
        super().__init__()
        self.zip_path = zip_path
        self.log_path = log_path
        self.current_dir = ''
        self.init_ui()
        self.load_zip_file()
        self.init_log()

    def init_ui(self):
        self.setWindowTitle('Shell Emulator')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Поле для ввода команд
        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Введите команду")
        self.command_input.returnPressed.connect(self.execute_command)
        self.layout.addWidget(self.command_input)

        # Поле для вывода результатов команд
        self.output_display = QTextEdit(self)
        self.output_display.setReadOnly(True)
        self.layout.addWidget(self.output_display)

        # Кнопка для очистки вывода
        self.clear_button = QPushButton("Очистить", self)
        self.clear_button.clicked.connect(self.clear_output)
        self.layout.addWidget(self.clear_button)

        self.setLayout(self.layout)

        # Устанавливаем стиль: черный фон и зеленый текст
        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: green;
            }
            QLineEdit {
                background-color: black;
                color: green;
                border: 1px solid green;
            }
            QTextEdit {
                background-color: black;
                color: green;
                border: 1px solid green;
            }
            QPushButton {
                background-color: black;
                color: green;
                border: 1px solid green;
            }
        """)

    def load_zip_file(self):
        try:
            self.zip_file = zipfile.ZipFile(self.zip_path, 'r')
            self.output_display.append(f"Загружен архив: {self.zip_path}")
        except FileNotFoundError:
            self.output_display.append(f"Ошибка: не удается открыть zip файл: {self.zip_path}")
            sys.exit(1)

    def init_log(self):
        # Создаем пустую структуру XML для лог-файла
        root = ET.Element('log')
        tree = ET.ElementTree(root)
        tree.write(self.log_path)  # Перезаписываем файл log.xml, очищая его

    def log_action(self, action, details):
        tree = ET.parse(self.log_path)
        root = tree.getroot()

        action_elem = ET.SubElement(root, 'action')
        action_elem.set('name', action)
        action_elem.text = details

        tree.write(self.log_path)

    def execute_command(self):
        command = self.command_input.text()
        if command:
            self.output_display.append(f"> {command}")
            self.process_command(command)
            self.command_input.clear()

    def process_command(self, command):
        if command == 'ls':
            self.ls()
        elif command.startswith('cd'):
            _, path = command.split(' ', 1)
            self.cd(path)
        elif command == 'exit':
            self.log_action('exit', 'Exited the shell emulator')
            self.close()
        elif command == 'clear':
            self.clear_output()
        elif command == 'uname':
            self.output_display.append(platform.system())
            self.log_action('uname', 'Displayed system name')
        else:
            self.output_display.append(f"Неизвестная команда: {command}")

    def ls(self):
        # Если находимся в корне архива
        if self.current_dir == '':
            # Отображаем файлы и папки, находящиеся в корне директории
            files = [f.filename[20:].replace('/', '') for f in self.zip_file.infolist() if
                     f.filename.startswith(self.current_dir)]

            # Удаляем элементы, которые полностью содержат другие элементы
            unique_files = []
            for file in files:
                # Проверяем, не содержит ли файл другого, более короткого, элемента
                if not any(file != other and file.startswith(other) for other in files):
                    unique_files.append(file)

            # Выводим уникальные файлы и папки
            self.output_display.append("\n".join(unique_files))
            self.log_action('ls', 'Listed directory contents')
            return

        else:
            # Отображаем файлы и папки, находящиеся в текущей директории
            files_in_current_dir = [
                f.filename[len(self.current_dir):].strip('/')
                for f in self.zip_file.infolist()
                if f.filename.startswith(self.current_dir) and f.filename != self.current_dir
            ]

        # Фильтрация только файлов и директорий верхнего уровня
        displayed_files = []
        for file in files_in_current_dir:
            # Показываем только файлы и директории, которые не содержат вложенных элементов
            if '/' not in file or file.endswith('/'):
                displayed_files.append(file)

        # Выводим содержимое текущей директории
        if displayed_files:
            self.output_display.append("\n".join(displayed_files))
        else:
            self.output_display.append("Папка пуста")

        self.log_action('ls', 'Listed directory contents')

    def cd(self, path):
        # Отладочный вывод текущей директории
        self.output_display.append(f"Текущая директория: {self.current_dir}")

        # Если введен "/", возвращаемся в корневую директорию
        if path == '/' or path == '~':
            self.current_dir = ''
            self.output_display.append("Перешли в корневую директорию.")
            self.log_action('cd', 'Changed directory to root')
            return

        # Обработка команды "cd .." для возврата на уровень вверх
        elif path == '..':
            if self.current_dir:
                # Убираем последний сегмент пути
                self.current_dir = '/'.join(self.current_dir.strip('/').split('/')[:-1])
                if self.current_dir:
                    self.current_dir += '/'  # Добавляем завершающий слеш, если путь не пуст
                self.output_display.append("Перешли на уровень выше.")
            else:
                self.output_display.append("Уже находимся в корневой директории.")
            self.log_action('cd', 'Changed directory to parent')
            return

        # Построим полный путь относительно текущей директории
        if self.current_dir == '':
            potential_dir = os.path.join('virtual_file_system', path).replace('\\', '/').rstrip('/') + '/'
        else:
            potential_dir = os.path.join(self.current_dir, path).replace('\\', '/').rstrip('/') + '/'

        # Отладочный вывод пути для перехода
        self.output_display.append(f"Пытаемся перейти в директорию: {potential_dir}")

        # Проверяем, существует ли такая директория в архиве
        if any(f.filename.startswith(potential_dir) and f.filename.endswith('/') for f in self.zip_file.infolist()):
            self.current_dir = potential_dir
            self.output_display.append(f"Перешли в директорию: {path}")
        else:
            self.output_display.append(f"Ошибка: директория {path} не найдена.")

        self.log_action('cd', f"Changed directory to {path}")

    def clear_output(self):
        self.output_display.clear()
        self.log_action('clear', 'Cleared output display')


def main():
    parser = argparse.ArgumentParser(description='Эмулятор командной оболочки')
    parser.add_argument('zip_path', help='Путь к zip-файлу виртуальной файловой системы')
    parser.add_argument('log_path', help='Путь к лог-файлу в формате XML')
    args = parser.parse_args()

    app = QApplication(sys.argv)
    emulator = ShellEmulator(args.zip_path, args.log_path)
    emulator.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
