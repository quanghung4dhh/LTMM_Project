## Modular.py:

- Đây là file thuật toán số học modulo, là nền tảng toán học của mật mã, gồm các hàm:

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

### Các thuật toán cần chú ý:

- Thuật toán gcd(a, b) dùng để tìm ước chung lớn nhất của 2 số nguyên a và b. Thuật toán này dựa trên thuật toán Euclid: gcd(a, b) = gcd(b, a mod b). Sơ đồ thuật toán như sau: <br>
  ![Thuật toán gcd](../assets/gcd.png)

- Thuật toán Euclid mở rộng:
  - Thuật toán này dùng để tìm hệ số Bézout x, y
  - Với đầu vào là 2 số nguyên a, b, đầu ra thuật toán là (g, x, y) thỏa mãn:
    <p align="center">
      <strong>ax + by = g = gcd(a, b)</strong>
    </p>
  - Sơ đồ thuật toán: <br>
    ![Thuật toán extended gcd](../assets/extended_gcd.png)
- Thuật toán tìm nghịch đảo nhân: Sử dụng thuật toán euclid mở rộng để tìm x rồi xuất ra giá trị x % m
- Thuật toán tìm Zn\*: Lặp qua từ 0 đến n rồi lấy các giá trị có gcd(a, n) = 1
