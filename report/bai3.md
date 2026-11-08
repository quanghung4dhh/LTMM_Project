## Mật mã chuyển vị (Transposition Cipher)

- Đối với mật mã thay thế, ta thay thế từng ký tự của bản rõ thành 1 ký tự khác, nhưng vẫn giwũ nguyên vị trí của các ký tự trong bản rõ
- Đối với mật mã chuyển vị, ta không thay thế các ký tự bản rõ thành 1 ký tự khác mà xáo trộn vị trí của các ký tự trong bản rõ
- VD: Với P = CAT
  - Nếu dùng mật mã thay thế là mật mã dịch thì C = DBU, dịch mỗi ký tự thêm 1 trong bảng chữ cái
  - Còn nếu dùng mật mã chuyển vị thì C = TCA, chỉ xáo trộn các ký tự trong P, không thêm hay tạo ra những kí tự khác

## 1. Lý thuyết hoán vị và Nhóm hoán vị (Permutation Theory &amp; Permutation Group)

- Phép hoán vị: Là phép sắp xếp lại thứ tự các vị trí các phần tử của một tập hợp.
- Phép hoán vị $\pi$ là một ánh xạ song ánh, là mô hình toán học định nghĩa mật mã chuyển vị khối độ dài t
- Phép hoán vị nghịch đảo (Inverse Permutation): Đây là phép giải mã $\pi^{-1}$ tương ứng với phép hoán vị $\pi$ sao cho $\pi^{-1}$ $\pi$ = I
- Nhóm hoán vị: Là nhóm tập hợp tất cả các hoán vị t phần tử, có tổng cộng t! phép hoán vị. Khi thực hiện mã hóa chuyển vị nhiều lần liên tiếp, kết quả vẫn sẽ tương đương với thực hiện 1 lần hoán vị duy nhất với t = lcm(t1,t2,t3,...): Bội chung nhơ nhất

## 2. Đại số tuyến tính và ma trận hoán vị (Permutation Matrices)

- Ma trận hoán vị: Khóa chuyển vị kích thước m được biểu diễn thành ma trận vuông khóa K kích thước mxm, trong đó mỗi hàng và mỗi cột có duy nhất 1 giá trị 1, còn lại là giá trị 0
- Mã hóa bằng phép nhân ma trận: C = PK
- Tính chất chuyển vị ma trận ($K^{-1} = K^T$): Để giải mã, ta nhân bản mã với ma trận nghịch đảo của khóa: P = $K^{-1}$ C = $K^T$ C
