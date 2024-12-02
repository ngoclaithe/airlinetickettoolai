class TextManager:
    def __init__(self, text=""):
        self.text = text

    def to_uppercase(self):
        return self.text.upper()

    def to_lowercase(self):
        return self.text.lower()

    def reverse_text(self):
        return self.text[::-1]

    def title_case(self):
        return self.text.title()

    def swap_case(self):
        return self.text.swapcase()

    def set_text(self, new_text):
        self.text = new_text

    def get_text(self):
        return self.text

if __name__ == "__main__":
    text_mgr = TextManager("ĐÂy là một vĂN bảN cầN SửA Hello World")

    print("Chữ hoa:", text_mgr.to_uppercase())
    print("Chữ thường:", text_mgr.to_lowercase())
    print("Đảo ngược:", text_mgr.reverse_text())
    print("Viết hoa từng từ:", text_mgr.title_case())
    print("Chuyển đổi hoa/thường:", text_mgr.swap_case())