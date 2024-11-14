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
