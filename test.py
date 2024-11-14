import unittest
import xml.etree.ElementTree as ET
from emulator import ShellEmulator
from PyQt5.QtWidgets import QApplication

# Запуск QApplication, требуется для работы с PyQt5
app = QApplication([])

class TestShellEmulatorSequence(unittest.TestCase):
    def setUp(self):
        # Путь к существующим файлам
        self.zip_path = 'virtual_file_system.zip'  # Убедитесь, что этот файл существует
        self.log_path = 'log.xml'  # Убедитесь, что этот файл существует

        # Создаем экземпляр ShellEmulator для тестирования
        self.emulator = ShellEmulator(self.zip_path, self.log_path)

    def test_command_sequence(self):
        # Последовательно вводим команды и проверяем вывод

        # uname
        self.emulator.process_command('uname')
        output = self.emulator.output_display.toPlainText().strip().split('\n')[-1]
        self.assertEqual(output, 'Windows')

        # Очищаем output_display перед следующей командой
        self.emulator.output_display.clear()

        # ls в корневой директории
        self.emulator.process_command('ls')
        output = self.emulator.output_display.toPlainText()
        self.assertIn('file1.txt', output)
        self.assertIn('folder1', output)
        self.assertIn('folder2', output)

        # Очищаем output_display перед следующей командой
        self.emulator.output_display.clear()

        # cd folder1
        self.emulator.process_command('cd folder1')
        output = self.emulator.output_display.toPlainText().strip().split('\n')[-1]
        self.assertIn('Перешли в директорию: folder1', output)

        # Очищаем output_display перед следующей командой
        self.emulator.output_display.clear()

        # ls в folder1
        self.emulator.process_command('ls')
        output = self.emulator.output_display.toPlainText()
        self.assertIn('file2.txt', output)
        self.assertNotIn('file1.txt', output)

        # Очищаем output_display перед следующей командой
        self.emulator.output_display.clear()

        # uname снова
        self.emulator.process_command('uname')
        output = self.emulator.output_display.toPlainText().strip().split('\n')[-1]
        self.assertEqual(output, 'Windows')

        # Очищаем output_display перед следующей командой
        self.emulator.output_display.clear()

        # cd .. (возврат на уровень выше)
        self.emulator.process_command('cd ..')
        output = self.emulator.output_display.toPlainText().strip().split('\n')[-1]
        self.assertIn('Перешли на уровень выше', output)

        # Очищаем output_display перед следующей командой
        self.emulator.output_display.clear()

        # ls в корне снова
        self.emulator.process_command('ls')
        output = self.emulator.output_display.toPlainText()
        self.assertIn('file1.txt', output)
        self.assertIn('folder1', output)
        self.assertIn('folder2', output)

        # Очищаем output_display перед следующей командой
        self.emulator.output_display.clear()

        # cd folder2
        self.emulator.process_command('cd folder2')
        output = self.emulator.output_display.toPlainText().strip().split('\n')[-1]
        self.assertIn('Перешли в директорию: folder2', output)

        # Очищаем output_display перед следующей командой
        self.emulator.output_display.clear()

        # cd ~ (возврат в корень)
        self.emulator.process_command('cd ~')
        output = self.emulator.output_display.toPlainText().strip().split('\n')[-1]
        self.assertIn('Перешли в корневую директорию.', output)

        # Очищаем output_display перед следующей командой
        self.emulator.output_display.clear()

        # clear (очистка вывода)
        self.emulator.process_command('clear')
        output = self.emulator.output_display.toPlainText().strip()
        self.assertEqual(output, '')  # Проверяем, что вывод очищен

        # uname в третий раз
        self.emulator.process_command('uname')
        output = self.emulator.output_display.toPlainText().strip().split('\n')[-1]
        self.assertEqual(output, 'Windows')

        # Очищаем output_display перед следующей командой
        self.emulator.output_display.clear()

        # exit (завершение работы)
        self.emulator.process_command('exit')
        # Проверка записи команды в лог
        tree = ET.parse(self.log_path)
        root = tree.getroot()
        self.assertEqual(root[-1].get('name'), 'exit')
