from flask import Flask, request, send_file, render_template_string, url_for
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def derive_key(key_str):
    key_bytes = key_str.encode('utf-8')
    return pad(key_bytes, 16)[:16]

def encrypt_data(data, key_str):
    key = derive_key(key_str)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return iv + ciphertext

def decrypt_data(data, key_str):
    key = derive_key(key_str)
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AES Encrypt & Decrypt</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <h2 class="text-center mb-4">🔐 AES File Encrypt & Decrypt</h2>
    <div class="row g-4">

        <!-- Encrypt Card -->
        <div class="col-md-6">
            <div class="card shadow-lg p-4 h-100">
                <h4 class="card-title mb-3">🔒 Mã hóa file</h4>
                {% if encrypt_message %}
                <div class="alert alert-{{ 'success' if encrypt_success else 'danger' }}" role="alert">
                    {{ encrypt_message|safe }}
                </div>
                {% endif %}
                <form method="POST" enctype="multipart/form-data">
                    <input type="hidden" name="form_type" value="encrypt">
                    <div class="mb-3">
                        <label class="form-label">Chọn file:</label>
                        <input type="file" name="file" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Nhập khóa:</label>
                        <input type="text" name="key" class="form-control" required>
                        <div class="form-text">Khóa có thể có độ dài tùy ý, sẽ chuẩn hóa 16 byte.</div>
                    </div>
                    <button type="submit" class="btn btn-success w-100">Mã hóa</button>
                </form>
            </div>
        </div>

        <!-- Decrypt Card -->
        <div class="col-md-6">
            <div class="card shadow-lg p-4 h-100">
                <h4 class="card-title mb-3">🔓 Giải mã file</h4>
                {% if decrypt_message %}
                <div class="alert alert-{{ 'success' if decrypt_success else 'danger' }}" role="alert">
                    {{ decrypt_message|safe }}
                </div>
                {% endif %}
                <form method="POST" enctype="multipart/form-data">
                    <input type="hidden" name="form_type" value="decrypt">
                    <div class="mb-3">
                        <label class="form-label">Chọn file (.enc):</label>
                        <input type="file" name="file" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Nhập khóa:</label>
                        <input type="text" name="key" class="form-control" required>
                        <div class="form-text">Khóa phải trùng với khóa khi mã hóa.</div>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Giải mã</button>
                </form>
            </div>
        </div>

    </div>
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    encrypt_message = None
    decrypt_message = None
    encrypt_success = False
    decrypt_success = False

    if request.method == 'POST':
        form_type = request.form.get('form_type')
        file = request.files.get('file')
        key = request.form.get('key')

        if not file or not key:
            msg = "Vui lòng nhập đầy đủ file và khóa!"
            if form_type == 'encrypt':
                encrypt_message = msg
            else:
                decrypt_message = msg
        else:
            filename = file.filename
            data = file.read()

            try:
                if form_type == 'encrypt':
                    encrypted_data = encrypt_data(data, key)
                    out_filename = filename + '.enc'
                    out_path = os.path.join(PROCESSED_FOLDER, out_filename)
                    with open(out_path, 'wb') as f:
                        f.write(encrypted_data)
                    download_url = url_for('download_file', filename=out_filename)
                    encrypt_message = f"Mã hóa thành công! <a href='{download_url}'>Tải file</a>"
                    encrypt_success = True

                elif form_type == 'decrypt':
                    decrypted_data = decrypt_data(data, key)
                    if filename.endswith('.enc'):
                        out_filename = filename[:-4] + '.dec'
                    else:
                        out_filename = filename + '.dec'
                    out_path = os.path.join(PROCESSED_FOLDER, out_filename)
                    with open(out_path, 'wb') as f:
                        f.write(decrypted_data)
                    download_url = url_for('download_file', filename=out_filename)
                    decrypt_message = f"Giải mã thành công! <a href='{download_url}'>Tải file</a>"
                    decrypt_success = True

                else:
                    if form_type == 'encrypt':
                        encrypt_message = "Hành động không hợp lệ."
                    else:
                        decrypt_message = "Hành động không hợp lệ."
            except Exception as e:
                error_msg = f"Lỗi: {str(e)}"
                if form_type == 'encrypt':
                    encrypt_message = error_msg
                else:
                    decrypt_message = error_msg

    return render_template_string(HTML_PAGE,
                                  encrypt_message=encrypt_message,
                                  decrypt_message=decrypt_message,
                                  encrypt_success=encrypt_success,
                                  decrypt_success=decrypt_success)

@app.route('/processed/<filename>')
def download_file(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
