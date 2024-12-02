import qrcode

# Đoạn mã code bạn muốn chuyển thành mã QR
data = "00020101021238570010A00000072701270006970422011314686515099990208QRIBFTTA530370454061000005802VN62070803abc63041F5F"

# Tạo đối tượng QR Code
qr = qrcode.QRCode(
    version=1,  # Chỉ định kích thước của mã QR (1 đến 40)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Mức độ sửa lỗi
    box_size=10,  # Kích thước của mỗi hộp (pixel)
    border=4,  # Kích thước của biên (số hộp)
)

# Thêm dữ liệu vào mã QR
qr.add_data(data)
qr.make(fit=True)

# Tạo hình ảnh QR
img = qr.make_image(fill="black", back_color="white")

# Lưu hoặc hiển thị hình ảnh
img.save("qr_code.png")
img.show()
