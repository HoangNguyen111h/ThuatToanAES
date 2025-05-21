# ThuatToanAES
<h2 align="center">Ứng dụng Mã hóa và Giải mã Dữ liệu bằng AES</h2>

<p>
Dự án bao gồm hai ứng dụng web riêng biệt, được xây dựng bằng Python và Flask, nhằm thực hiện việc bảo mật dữ liệu bằng thuật toán AES (Advanced Encryption Standard).
</p>

<h3>Chức năng của ứng dụng</h3>

<ul>
  <li><strong>Ứng dụng Mã hóa (Encrypt):</strong>
    <ul>
      <li>Nhập khóa bí mật bất kỳ</li>
      <li>Tải lên file dữ liệu bất kỳ</li>
      <li>Mã hóa nội dung bằng thuật toán AES</li>
      <li>Tải về file đã được mã hóa</li>
    </ul>
  </li>
  <li><strong>Ứng dụng Giải mã (Decrypt):</strong>
    <ul>
      <li>Nhập đúng khóa đã dùng khi mã hóa</li>
      <li>Tải lên file đã mã hóa</li>
      <li>Giải mã và tải về file gốc</li>
    </ul>
  </li>
</ul>

<h3>Công nghệ sử dụng</h3>

<ul>
  <li>Python 3</li>
  <li>Flask</li>
  <li>HTML thuần</li>
  <li>Thuật toán AES</li>
</ul>

<h3>Hướng dẫn sử dụng</h3>

<ol>
  <li>Cài đặt thư viện: <code>pip install flask pycryptodome</code></li>
  <li>Chạy ứng dụng mã hóa: <code>python encrypt_app.py</code></li>
  <li>Chạy ứng dụng giải mã: <code>python decrypt_app.py</code></li>
  <li>Truy cập hai ứng dụng tại hai địa chỉ localhost khác nhau (ví dụ: <code>localhost:5000</code> và <code>localhost:5001</code>)</li>
</ol>

<h3>Giao diện ứng dụng</h3>

<p><strong>1. Giao diện ứng dụng mã hóa và giải mã:</strong></p>
<p align="center">
  <img src="https://github.com/hiepnguyen05/ThuatToanAES/blob/main/screenshots/encrypt_interface.png?raw=true" alt="Giao diện mã hóa" width="600">
</p>



<p><strong>Tác giả:</strong> Nguyễn Ngọc Hiệp - Khoa Công nghệ thông tin, Đại học Đại Nam</p>
