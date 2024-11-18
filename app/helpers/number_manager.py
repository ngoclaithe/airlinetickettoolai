import math
from vietnam_number import n2w

class NumberManager:
    def __init__(self):
        pass

    def convert_number_to_words(self, number):
        """Chuyển đổi số thành chữ (tiếng Việt)"""
        words = n2w(number)
        return words

    def calculate_vat_forward(self, amount, vat_rate):
        """
        Tính số VAT xuôi.
        :param amount: Số gốc.
        :param vat_rate: Phần trăm VAT.
        :return: Tổng số tiền sau khi thêm VAT.
        """
        return round(amount + (amount * vat_rate / 100))

    def calculate_vat_reverse(self, amount, vat_rate):
        """
        Tính số VAT ngược.
        :param amount: Tổng số tiền đã bao gồm VAT.
        :param vat_rate: Phần trăm VAT.
        :return: Số tiền gốc.
        """
        return round(amount / (1 + vat_rate / 100))

    def calculate_percentage(self, percentage, amount):
        """
        Tính % của một số.
        :param percentage: Phần trăm muốn tính.
        :param amount: Số gốc.
        :return: Kết quả của phép tính %.
        """
        return (percentage / 100) * amount

