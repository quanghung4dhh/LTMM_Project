## File modular.py:

### 1. Số học modulo:

- normalize_mod(a, m): Chuẩn hóa số về khoảng 0 đến m-1
- add_mod(a, b, m): Cộng modulo
- substract_mod(a, b, m): Trừ modulo
- multiply_mod(a, b, m): Nhân modulo

### 2. Thuật toán Euclid:

- gcd(a, b): Tìm ước chung lớn nhất
- extended(a, b): Tìm gcd và 2 hệ số Bezout
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
- matrix_inverse_mod(n): Tìm ma trận nghịch đảo modulo

## File test_matrix.py:

- Gồm 52 bài test file matrix.py
