<h1 align="center">Домашняя работа №1 - Эмулятор для языка оболочки ОС</a> 
<h3 align="center">Постановка задачи</h3>
  
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу 
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. 
Эмулятор должен запускаться из реальной командной строки, а файл с 
виртуальной файловой системой не нужно распаковывать у пользователя. 
Эмулятор принимает образ виртуальной файловой системы в виде файла формата 
zip. Эмулятор должен работать в режиме GUI. 

Ключами командной строки задаются: 
• Путь к архиву виртуальной файловой системы. 
• Путь к лог-файлу.

Лог-файл имеет формат xml и содержит все действия во время последнего 
сеанса работы с эмулятором.

Необходимо поддержать в эмуляторе команды ls, cd и exit, а также 
следующие команды: 
1. clear. 
2. uname.
   
Все функции эмулятора должны быть покрыты тестами, а для каждой из 
поддерживаемых команд необходимо написать 3 теста.

### Запуск программы
```bash
cd:\Users\user\PycharmProjects\emulator
.venv\Scripts\activate
python emulator.py virtual_file_system.zip log.xml
```

### Результаты тестов

![image](https://github.com/user-attachments/assets/71e1cb1b-efa9-49ab-82fb-a996ad364629)


### Скрины работы программы
- Комманда ``ls``
  
![image](https://github.com/user-attachments/assets/db9891a6-631c-4cfd-a718-0643a55be91b)


- Комманда ``cd``

![image](https://github.com/user-attachments/assets/6548fcc4-c99c-4719-9659-463268cce2d5)


- Комманда ``uname``

![image](https://github.com/user-attachments/assets/83322039-36c7-4750-96ca-6736c0b60c22)


- Комманда ``clear``

![image](https://github.com/user-attachments/assets/e777e1b4-75d6-44b7-84ec-1f9c8bdb3384)


![image](https://github.com/user-attachments/assets/4f18921f-c273-4f0c-8c68-3a0d3c7d00ae)


- Комманда ``exit``

![image](https://github.com/user-attachments/assets/7eedc1b6-c81c-4dac-b40c-75ce17807600)

![image](https://github.com/user-attachments/assets/92777821-1c1c-4921-a934-d22763c70890)


