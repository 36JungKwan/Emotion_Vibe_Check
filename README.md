# AI XÚC CẢM - CẢM NẮNG AI 🎭
Một trò chơi nhóm thú vị sử dụng AI để nhận diện cảm xúc và đưa ra thử thách độc đáo.

## 💡 Giới thiệu
- Ứng dụng sử dụng webcam để: Nhận diện cảm xúc khuôn mặt của người chơi bằng AI (DeepFace).

- Gợi ý thử thách biểu cảm dựa trên cảm xúc được chọn.

- Tính toán mức độ giống biểu cảm và chọn người biểu cảm kém nhất để thực hiện thử thách.

- Cho phép lưu lại ảnh + kết quả và trích xuất ra CSV.

- Ứng dụng được phát triển bằng Python với PyQt5 GUI và thư viện DeepFace cho AI cảm xúc.

## 📷 Cách chơi
- Mở ứng dụng.

- Nhấn "Bắt đầu chơi", AI sẽ chọn một cảm xúc ngẫu nhiên.

- Cả nhóm thể hiện cảm xúc đó trước webcam.

- Sau 5 giây, AI sẽ phân tích và chọn người có điểm thấp nhất cho cảm xúc yêu cầu.

- Một thử thách vui nhộn sẽ xuất hiện cho người đó thực hiện.

- Bạn có thể lưu kết quả để chia sẻ lên mạng xã hội và nhận quà 🎁.

## 📦 Cài đặt

**Clone repo về máy**

git clone https://github.com/36JungKwan/Emotion_Vibe_Check

**Cài đặt thư viện cần thiết**

pip install -r requirements.txt

## ▶️ Chạy ứng dụng

python app.py

## 📁 Kết quả lưu
Ảnh chụp khuôn mặt được lưu trong thư mục snapshots/.

File results.csv lưu thông tin:

- Timestamp

- Emotion chủ đạo

- Điểm các cảm xúc khác

- Gợi ý thử thách

- Đường dẫn ảnh

## 🧠 Công nghệ sử dụng
| Thư viện         | Mô tả                                   |
| ---------------- | --------------------------------------- |
| **PyQt5**        | Xây dựng giao diện người dùng đẹp mắt   |
| **OpenCV**       | Truy cập webcam và xử lý ảnh            |
| **DeepFace**     | Nhận diện khuôn mặt & phân tích cảm xúc |
| **Pandas/Numpy** | Xử lý dữ liệu                           |
| **CSV/Datetime** | Lưu kết quả trò chơi                    |


## 💚 Tính năng nổi bật
✅ Nhận diện nhiều khuôn mặt cùng lúc

✅ Hiệu ứng bóng đổ, màu sắc giao diện hài hòa

✅ Hiển thị ảnh khuôn mặt + gợi ý thử thách tương tác

✅ Chơi vui – học AI – tạo kỷ niệm đáng nhớ

## 📸 Gợi ý dùng
Làm trò chơi nhóm trong lớp học, workshop, câu lạc bộ

Triển lãm công nghệ AI tại các sự kiện trường học

Làm minigame trên sân khấu với camera

## ✨ Ghi chú
- Thay đổi các path (đường dẫn) nếu cần
- Lần đầu chạy app sẽ khá tốn thời gian vì các thư viện sẽ tự động tải model (DeepFace) về nếu chưa có
