## 4.1 Phân tích tần suất (Frequency analysis)

- Phân tích tần suất (Frequency analysis) là một kỹ thuật thám mã cổ điển, dựa trên việc thống kê số lần xuất hiện của các ký tự trong bản mã hoặc bản rõ
- Phương pháp này khai thác đặc điểm thống kê của ngôn ngữ tự nhiên. Ví dụ như trong tiếng Anh, các chữ cái như E, T, A, O thường xuất hiện nhiều hơn so với J, Q, X, Z

- Bằng cách thống kê và sắp xếp các chữ cái theo tần suất xuất hiện, người phân tích mật mã có thể đưa ra những giả thuyết về ánh xạ giữa chữ cái trong bảng mã và chữ cái trong bản rõ

- Trong phạm vi bài tập lớn, thuật toán sẽ tập trung vào việc:
  - Trích xuất các chữ cái tiếng Anh hợ lệ của từng chữ cái
  - Đếm số lần xuất hiện của từng chữ cái
  - Tính tần suất tương đối của từng chữ cái
  - Sắp xếp các chữ cái theo tần suất giảm dần

### 4.1.1 Cơ sở lý thuyết

- Ta có:

```math
P(c)=\frac{f(c)}{N}
```

- Trong đó:
  - P(c) là tần suất tương đối của chữ cái c
  - N là tổng chữ cái hợp lệ trong văn bản (Các chữ cái từ A-Z)
  - f(c) là số lần xuất hiện của chữ cái c trong văn bản

### 4.1.2. Vai trò của phân tích tần suất trong thám mã

- Phân tích tần suất có thể hỗ trợ phá một số hệ mã cổ điển: như mật mã thay thế đơn bảng chữ cái, mật mã chuyển vị và mật mã đa bảng chữ cái như Vigenere

### 4.1.3. Cài đặt và thiết kế thuật toán

![Frequency Analysis](../assets/freq.png)
<br>
