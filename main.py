import itertools
import os
import re
import sys
from datetime import date
from os.path import exists
from typing import Match


headers = "Номер п/п, Дата, Категория, Сумма, Описание"


def number_unique(numb: str) -> bool:
    """
    Проверка на уникальность введенного номера записи.
    :param numb: номер записи введенные пользователем
    """
    numb_list: list = []
    with open("files/wallet.txt", "r") as file:
        for line in itertools.islice(file, 1, None):
            line_list: list[str] = [elem.strip() for elem in line.split(",")]
            numb_list.append(line_list[0])
        return all(numb != n for n in numb_list)


def correct_data(data: str) -> bool:
    """
    Проверка на валидность введенных данных.
    :param data: данные введенные пользователем
    """
    category_list: list[str] = ["Доходы", "Расходы"]
    data_list: list[str] = [elem.strip() for elem in data.split(",")]
    try:
        res: bool = (
            isinstance(int(data_list[0]), int)
            and bool(date.fromisoformat(data_list[1]))
            and data_list[2] in category_list
            and isinstance(int(data_list[3]), int)
            and isinstance(data_list[4], str)
        )
    except ValueError:
        res: bool = False
    return res


class PersonanalWallet:
    """
    Класс для работы с личным финансовым кошельком
    """

    def __init__(self, filename: str) -> None:
        self.filename = filename


    def create_txt_file(self):
        """
        Метод класса для создания .txt файла
        """
        path: str = self.filename
        if exists(path):
            print("Личный финансовый кошелек уже существует!")
        else:
            with open(path, "w", encoding="utf-8") as file:
                file.write(headers + "\n")

    def get_balance_info(self) -> int:
        """
        Метод класса для получения информации о балансе кошелька, расходах и доходах
        """

        balance_type: int = int(
            input(
                "Введите номер задачи для получения информации о балансе: \n"
                "1 - Показать текущий баланс \n"
                "2 - Показать расходы \n"
                "3 - Показать доходы \n"
            )
        )
        with open(self.filename, "r") as file:
            balance: int = 0
            for line in itertools.islice(file, 1, None):
                income: Match[str] = re.search(r"\bДоходы\b", line)
                expenditure: Match[str] = re.search(r"\bРасходы\b", line)
                if balance_type == 1:
                    if expenditure:
                        balance -= int(line.split(",")[3])
                    elif income:
                        balance += int(line.split(",")[3])
                elif balance_type == 2:
                    if expenditure:
                        balance -= int(line.split(",")[3])
                elif balance_type == 3:
                    if income:
                        balance += int(line.split(",")[3])
            return balance

    def add_balance_info(self) -> bool:
        """
        Метод класса для добавления записи в кошелек
        """
        while True:
            new_balance_data: str = input(
                "Введите данные о расходах или доходах через запятую (Пример '1, 2024-03-02, Расходы, 550, Покупка лекарств'): \n"
            )
            with open(self.filename, "a") as file:
                if correct_data(new_balance_data) and number_unique(
                    new_balance_data[0]
                ):
                    file.write(new_balance_data + "\n")
                    return True
                else:
                    print("Введены некорректные данные!")
                    continue

    def update_balance_info(self) -> bool:
        """
        Метод класса для редактирования записи
        """
        while True:
            search_post: str = input("Введите порядковый номер редактируемой записи: ")
            with open(self.filename, "r") as file:
                lines: list[str] = file.readlines()
                for i in range(len(lines)):
                    if lines.index(lines[i]) == int(search_post):
                        replace_text: str = input(f"Отредактируйте запись: {lines[i]}")
                        lines[i] = replace_text + "\n"
                        if correct_data(lines[i]) and search_post == replace_text[0]:
                            with open(self.filename, "w") as file:
                                file.writelines(lines)
                                return True
                        else:
                            print("Введены некорректные данные!")
                            continue

    def search_balance_info(self) -> None:
        """
        Основной метод класса для поиска информации о записях
        """
        while True:
            search_type: int = int(
                input(
                    "Введите номер задачи для поиска записей: \n"
                    "1 - Поиск записей по категории \n"
                    "2 - Поиск записей по дате \n"
                    "3 - Поиск записей по сумме \n"
                )
            )

            if search_type == 1:
                result = self.search_from_type()
                if result == None:
                    print("Введите корреткную категорию!")
                    continue
                for res in result:
                    print(res)
                break
            elif search_type == 2:
                result = self.search_from_date()
                if result:
                    for res in result:
                        print(res)
                    break
            elif search_type == 3:
                result = self.search_from_sum()
                if result:
                    for res in result:
                        print(res)
                    break
            else:
                print("Введите корректное число!")

    def search_from_type(self) -> list[str]:
        """
        Метод класса для поиска информации о записях по категории
        """
        with open(self.filename, "r") as file:
            info_list = []
            lines: list[str] = file.readlines()
            category_list: list[str] = ["Доходы", "Расходы"]
            category: str = input("Введите название категории (Доходы, Расходы): \n")
            if category in category_list:
                for line in lines[1:]:
                    line_list: list[str] = [elem.strip() for elem in line.split(",")]
                    if category in line_list:
                        info_list.append(line[:-1])
                return info_list

    def search_from_date(self) -> list[str]:
        """
        Метод класса для поиска информации о записях по дате
        """
        with open(self.filename, "r") as file:
            info_list = []
            lines: list[str] = file.readlines()
            date_balance: str = input("Введите дату в формате (гггг-мм-дд): \n")
            if date.fromisoformat(date_balance):
                for line in lines[1:]:
                    line_list: list[str] = [elem.strip() for elem in line.split(",")]
                    if date_balance in line_list:
                        info_list.append(line[:-1])
            return info_list

    def search_from_sum(self) -> list[str]:
        """
        Метод класса для поиска информации о записях по сумме
        """
        with open(self.filename, "r") as file:
            list_info = []
            lines: list[str] = file.readlines()
            sum_balance: str = input("Введите сумму для поиска: \n")
            if isinstance(int(sum_balance), int):
                for line in lines[1:]:
                    line_list: list[str] = [elem.strip() for elem in line.split(",")]
                    if sum_balance in line_list:
                        list_info.append(line[:-1])
            return list_info

    def exit_wallet(self) -> None:
        """
        Метод класса для остановки работы с персональным кошельком.
        """
        print("Работа завершена!")
        sys.exit()

    def delete_wallet(self) -> None:
        """
        Функция для удаления персонального кошелька.
        """
        os.remove(self.filename)
        print("Персональный кошелёк удален!")


def wallet_work() -> None:
    """
    Основная функция для управления персональным кошельком
    """
    while True:
        try:
            wallet = PersonanalWallet("files/wallet.txt")
            action = int(
                input(
                    "Выберите действие для работы с персональным кошельком: \n"
                    "1 - Создать персональный кошелек  \n"
                    "2 - Вывод баланса: Показать текущий баланс, а также отдельно доходы и расходы  \n"
                    "3 - Добавление записи: Возможность добавления новой записи о доходе или расходе \n"
                    "4 - Редактирование записи: Изменение существующих записей о доходах и расходах \n"
                    "5 - Поиск по записям: Поиск записей по категории, дате или сумме \n"
                    "6 - Завершить работу с персогнальным кошельком \n"
                    "7 - Удалить персональный кошелек \n"
                )
            )
            if action == 1:
                wallet.create_txt_file()
            elif action == 2:
                print(wallet.get_balance_info())
            elif action == 3:
                wallet.add_balance_info()
            elif action == 4:
                wallet.update_balance_info()
            elif action == 5:
                wallet.search_balance_info()
            elif action == 6:
                wallet.exit_wallet()
            elif action == 7:
                wallet.delete_wallet()
            else:
                print("Введите число от 1 до 7 для корректной работы кошелька!")
                continue
        except Exception as ex:
            print("Ошибка!", str(ex))


if __name__ == "__main__":
    wallet_work()
