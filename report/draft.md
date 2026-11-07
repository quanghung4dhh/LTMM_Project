## File modular.py:

### 1. Số học modulo:

- normalize_mod(a, m): Chuẩn hóa số về khoảng 0 đến m-1
- add_mod(a, b, m): Cộng modulo
- subtract_mod(a, b, m): Trừ modulo
- multiply_mod(a, b, m): Nhân modulo

### 2. Thuật toán Euclid:

- gcd(a, b): Tìm ước chung lớn nhất
- extended_gcd(a, b): Tìm gcd và 2 hệ số Bezout
- is_coprime(a, b): Kiểm tra nguyên tố cùng nhau

### 3. Nghịch đảo nhân modulo: mod_inverse(a, m)

### 4. Zn và Zn\*:

- zn_elements(m): Liệt kê các phần tử Zn
- zn_star(m): Liệt kê các phần tử Zn\*
- is_in_zn_star(a, m): Kiểm tra xem phần tử có ở trong Zn\* không

## File test_modular.py:

- Gồm 50 bài test gồm các giá trị đặc biệt như số 0, số âm để test logic trong file modular.py

## File matrix.py:

- validate_matrix(): Kiểm tra ma trận hợp lệ
- matrix_add_mod(): Cộng modulo hai ma trận
- matrix_multiply_mod(): Nhân modulo 2 ma trận
- determinant(): Tính định thức
- matrix_inverse_mod(matrix, modulus): Tìm ma trận nghịch đảo modulo

## File test_matrix.py:

- Gồm 52 bài test file matrix.py

- Một số code Python:
  - assert <condition>: Đảm bảo điều kiện để chạy tiêp chương trình. Nếu không thỏa mãn điều kiện sẽ dừng chương trình và báo lỗi AssertionError
  - raise: dùng để ném lỗi ra ngoài
  - isinstance(object, classInfo): Kiểm tra điều kiện đối tượng object có thuộc kiểu dữ liệu classInfo hay không
  - Kiểu dữ liệu bytes: Kiểu dữ liệu nhị phân

=====================================================================================================

## File classical.common:

- is_ascii_letter(char)->bool: Xác định 1 ký tự có thuộc A-Z không
- char_to_number(char)->int: Chuyển ký tự đầu vào thành số nguyên 0-25 tương ứng
- number_to_char(int, uppercase=True)->char: Chuyển số thành ký tự tương ứng
- normalize_alpha_key(str)->str: Kiểm tra và chuẩn hóa khóa
- iter_alpha_position(str)->iterator: Duyệt các vị trí chứa A-Z

## File classical.substitution:

- shift_encrypt(plain, key): mã hóa shift cipher
- shift_decrypt(cipher, key): giải mã shift cipher
- \_shift_text(text, key, decrypt): Hàm xử lý chung cho shift cipher
- multiplicative_encrypt(): Mã hóa Multiplicative cipher
- multiplicative_decrypt(): Giải mã Multiplicative cipher
- \_multiplicative_text(): Xử lý chung cho Multiphicative cipher
- affine_encrypt(): Mã hóa affine
- affine_decrypt(): Giải mã affine
- \_affine_text(): Hàm xử lý chung cho affine cipher

## File classical.vigenere:

- vigenere_encrypt(): Mã hóa vigenere
- vigenere_decrypt(): Giải mã vigenere
- \_vigenere_text(): Hàm xử lý chung cho vigenere cipher

## File classical.autokey:

- autokey_encrypt(): Mã hóa autokey
- autokey_decrypt(): Giải mã autokey
- \_autokey_text(): Hàm xử lý chung cho autokey cipher
