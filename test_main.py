import unittest
from main import PersonanalWallet


wallet_test = PersonanalWallet("files/wallet_test.txt")


class WaleetTest(unittest.TestCase):

    def setUp(self) -> None:
        """
        Функция для инициализации тестового файла
        """
        self.testfile = open("files/wallet_test.txt")
        self.testdata = self.testfile.readlines()
        self.testfile.close()

    def test1_get_balance_info(self) -> None:
        """
        Тест функцию для получения информации о балансе кошелька, расходах и доходах
        """
        self.assertEqual(wallet_test.get_balance_info() if 1 else None, 13300)
        self.assertEqual(wallet_test.get_balance_info() if 2 else None, -1700)
        self.assertEqual(wallet_test.get_balance_info() if 3 else None, 15000)

    def test2_search_balance_info(self) -> None:
        """
        Тест функции для поиска информации о записях
        """
        test_type_income = [
            "2, 2024-03-03, Доходы, 10000, Зарплата",
            "3, 2024-03-04, Доходы, 5000, Инвестиции",
        ]
        test_type_expenditure = [
            "1, 2024-03-02, Расходы, 1500, Покупка продуктов",
            "4, 2024-03-05, Расходы, 200, Посещение бассейна",
        ]
        test_type_date = ["1, 2024-03-02, Расходы, 1500, Покупка продуктов"]
        test_type_sum = ["2, 2024-03-03, Доходы, 10000, Зарплата"]
        self.assertEqual(
            wallet_test.search_from_type() if "Доходы" else None, test_type_income
        )
        self.assertEqual(
            wallet_test.search_from_type() if "Расходы" else None, test_type_expenditure
        )
        self.assertEqual(
            wallet_test.search_from_date() if "2024-03-02" else None, test_type_date
        )
        self.assertEqual(
            wallet_test.search_from_sum() if "10000" else None, test_type_sum
        )

    def test3_add_balance_info(self) -> None:
        """
        Тест функции для добавления записи в кошелек
        """
        self.testfile_2 = open("files/wallet_test.txt")
        test_add_info = "5, 2024-03-05, Доходы, 200, Подарок\n"
        wallet_test.add_balance_info() if test_add_info else None
        self.testdata_2 = self.testfile_2.readlines()
        self.testfile_2.close()
        self.assertEqual(len(self.testdata_2), len(self.testdata) + 1)

    def test4_update_balance_info(self) -> None:
        """
        Тест функции для редактирования записи
        """
        self.testfile_3 = open("files/wallet_test.txt")
        test_update_info = "5, 2024-03-05, Доходы, 1200, Подарок\n"
        wallet_test.update_balance_info() if test_update_info else None
        self.testdata_3 = self.testfile_3.readlines()
        self.testfile_3.close()
        self.assertTrue(test_update_info in self.testdata_3)


if __name__ == "__main__":
    unittest.main()
