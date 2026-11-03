## Modular.py:

- Đây là file thuật toán số học modulo, là nền tảng toán học của mật mã, gồm các hàm:

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

======================================================================================================

## File matrix.py

- Đây là file gồm các thuật toán về ma trận, là nền tảng cho hệ mật mã dùng ma trận, có các hàm:
  - validate_matrix(): Kiểm tra ma trận hợp lệ
  - matrix_add_mod(): Cộng modulo hai ma trận
  - matrix_multiply_mod(): Nhân modulo 2 ma trận
  - determinant(): Tính định thức
  - matrix_inverse_mod(matrix, modulus): Tìm ma trận nghịch đảo modulo

### 1. validate_matrix(matrix, square: bool)

- Đây là hàm dùng để kiểm tra tính hợp lệ của ma trận, đảm bảo ma trận dầu vào của các thuật toán mã hóa là hợp lệ, tránh gây ra những lỗi không mong muốn
- Các điều kiện kiểm tra:
  - Kiểm tra cấu trúc đầu vào: đảm bảo đầu vào là cấu trúc sequence dạng [[hàng1], [hàng2]...] hoặc ((hàng1), (hàng2)...), không chấp nhận kiểu dữ liệu khác
  - Kiểm tra ma trận rỗng: Ma trận phải có ít nhất một hàng và mỗi hàng phải có ít nhất 1 phần tử
  - Kiểm tra tính đầy đủ: Tất cả hàng phải có cùng số lượng phần tử
  - Kiểm tra kiểu dữ liệu: Mỗi phần tử của ma trận phải là số nguyên, không chấp nhận kiểu dữ liệu khác như số thực, boolean
  - Kiểm tra ma trận vuông: Khi square = True, số hàng phải bằng số cột
- Cách thuật toán hoạt động:
  - Thuật toán sẽ duyệt qua từng hàng của ma trận. Số phần tử của hàng đầu tiên được dùng để làm số hàng chuẩn để so sánh với các hàng sau, đảm bảo cấu trúc đầy đủ tính chữ nhật của ma trận
  - Sau khi kiểm tra toàn bộ phần tử và kích thước, thuật toán sẽ kiểm tra điều kiện ma trận vuông nếu được yêu cầu
  - Đầu ra của hàm sẽ trả về ValuError hoặc TypeError với lỗi tương ứng nếu không thỏa mãn các điều kiện. Ngược lại sẽ trả về tuple gồm (r, c) gồm số hàng và số cột của ma trận
- Lưu đồ thuật toán<br>
  ![Thuật toán validate matrix](../assets/validate_matrix.png)

### 2. matrix_add_mod(left, right, modulus):

- Hàm matrix_add_mod dùng để thực hiện phép cộng ha ma trận có cùng kích thước theo modulo m. Kết quả của phép toán gồm các phần tử được chuẩn hóa về khoảng 0 đến m-1
- Hàm sẽ kiểm tra tính hợp lệ của ma trận trước bằng validate_matrix, rồi kiểm tra kích thước của 2 ma trận
- Nếu 2 ma trận có kích thước khác nhau thì sẽ báo lỗi
- Ngược lại, sẽ tiến hành cộng từng phần tử của 2 ma trận:
  <p align="center">
    <strong>Cij = (Aij + Bij) mod m</strong>
  </p>
- Lưu đồ thuật toán: <br>
  ![Thuật toán matrix add mod](../assets/matrix_add_modulo.png)
