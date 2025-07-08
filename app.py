from deepface import DeepFace
import sys
import os
import cv2
import random
import csv
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTableWidgetItem,
    QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QTableWidget, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation

class FaceAnalyzer:
    def detect_faces(self, frame_rgb):
        results = DeepFace.analyze(frame_rgb, actions=['emotion'], enforce_detection=False)
        faces = []

        if isinstance(results, list):
            for r in results:
                faces.append({
                    "bbox": r["region"],
                    "dominant_emotion": r["dominant_emotion"]
                })
        else:
            r = results
            faces.append({
                "bbox": r["region"],
                "dominant_emotion": r["dominant_emotion"]
            })

        for f in faces:
            region = f["bbox"]
            if isinstance(region, dict):
                x = region.get("x", 0)
                y = region.get("y", 0)
                w = region.get("w", 0)
                h = region.get("h", 0)
                f["bbox"] = (x, y, x + w, y + h)
            else:
                f["bbox"] = (0, 0, 0, 0)
        return faces

class FaceGameApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI XÚC CẢM - CẢM NẮNG AI")
        self.setGeometry(100, 100, 1200, 800)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 14px;
                color: #2e2e2e;
            }
            QMainWindow {
                background-color: #007ACC;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
            }
            QTextEdit {
                font-size: 20px;
            }
            QTableWidget {
                font-size: 20px;
            }
            QHeaderView::section {
                background-color: #e1e1e1;
                padding: 4px;
                font-size: 20px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QTableWidget, QTextEdit {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #d0d0d0;
                padding: 10px;
            }
        """)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setContentsMargins(1, 1, 1, 1)
        self.image_label.setFixedSize(1200,950)
        self.image_label.setStyleSheet("""
            border-radius: 15px;
            border: 3px solid #ccc;
            background-color: #66B2FF;
        """)
        self.apply_shadow(self.image_label)

        self.start_button = QPushButton("🎭 Bắt đầu chơi")
        self.start_button.setStyleSheet(self.button_style())
        self.start_button.clicked.connect(self.start_game)

        self.save_button = QPushButton("📥 Lưu kết quả")
        self.save_button.setStyleSheet(self.button_style())
        self.save_button.clicked.connect(self.save_result)

        self.info_label = QLabel("Nhấn vào 'Bắt đầu chơi' để bắt đầu!")
        self.info_label.setStyleSheet("""
            background-color: white;
            border-radius: 16px;
            padding: 16px 24px;
            font-size: 24px;
            font-weight: bold;
            color: green;
            border: 1px solid #e0e0e0;
        """)
        self.apply_shadow(self.info_label)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Người chơi", "Chỉ số cảm xúc (%)"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setFixedHeight(200)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #66B2FF;
                border: 1px solid #ccc;
                border-radius: 12px;
            }
            QWidget {background-color: #66B2FF;}
        """)
        self.apply_shadow(self.table)

        self.suggestion_box = QTextEdit()
        self.suggestion_box.setReadOnly(True)
        self.suggestion_box.setPlaceholderText("🤖 Thử thách sẽ hiện tại đây...")
        self.suggestion_box.setStyleSheet("""
            background-color: #66B2FF;
            border: 1px solid #ccc;
            border-radius: 12px;
            padding: 12px;
            color: white;
            font-size: 30px;
        """)
        self.apply_shadow(self.suggestion_box)

        self.face_label = QLabel()
        self.face_label.setFixedSize(200, 200)
        self.face_label.setStyleSheet("""
            QLabel {
                background-color: #66B2FF;
                border-radius: 12px;
                border: 1px solid #cccccc;
                padding: 5px;
            }
        """)
        self.apply_shadow(self.face_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.save_button)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(12)
        right_layout.addLayout(button_layout)
        right_layout.addWidget(self.info_label)
        right_layout.addWidget(QLabel("📊 Phân tích cảm xúc:"))

        left_of_right = QVBoxLayout()
        left_of_right.addWidget(self.table)

        right_of_right = QVBoxLayout()
        right_of_right.addWidget(self.face_label)

        self.right_content_layout = QHBoxLayout()
        self.right_content_layout.addLayout(left_of_right)
        self.right_content_layout.addLayout(right_of_right)
        right_layout.addLayout(self.right_content_layout)

        right_layout.addWidget(QLabel("🎯 Thử thách:"))
        right_layout.addWidget(self.suggestion_box)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.addWidget(self.image_label, 2)
        main_layout.addLayout(right_layout, 1)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        container.setStyleSheet("background-color: #005F9E;")

        self.cap = cv2.VideoCapture(0)
        self.face_analyzer = FaceAnalyzer()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown = 7

        self.current_frame = None
        self.target_emotion = ""
        self.detecting = False

        self.showMaximized()

    def button_style(self):
        return ("""
            QPushButton {
                background-color: green;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 23px;
            }
            QPushButton:hover {
                background-color: #006400;
            }
            QPushButton:pressed {
                background-color: #004B49;
            }
        """)
    
    def fade_in_widget(self, widget, duration=400):
        widget.setWindowOpacity(0)
        widget.setVisible(True)
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.start()
        # Giữ animation lại nếu cần (tránh bị GC)
        self._current_animation = animation

    def apply_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)               # Độ mờ của bóng
        shadow.setXOffset(0)                   # Độ lệch ngang
        shadow.setYOffset(4)                   # Độ lệch dọc
        shadow.setColor(QColor(0, 0, 0, 160))  # Màu bóng (đen, độ mờ 160)
        widget.setGraphicsEffect(shadow)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        self.current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = self.face_analyzer.detect_faces(self.current_frame)

        for face in faces:
            x1, y1, x2, y2 = face["bbox"]
            emotion = face["dominant_emotion"]
            cv2.rectangle(self.current_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(self.current_frame, emotion, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        image = QImage(self.current_frame, self.current_frame.shape[1], self.current_frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def start_game(self):
        self.target_emotion = random.choice(['happy', 'sad', 'angry', 'surprise', 'fear', 'disgust', 'neutral'])
        self.info_label.setText(f"😮 Hãy làm mặt: {self.target_emotion.upper()} – sẵn sàng trong 5 giây...")
        self.countdown = 5
        self.countdown_timer.start(1000)

    def update_countdown(self):
        self.countdown -= 1
        if self.countdown > 0:
            self.info_label.setText(f"⏳ Diễn theo biểu cảm '{self.target_emotion.upper()}' trong {self.countdown} giây...")
        else:
            self.countdown_timer.stop()
            self.info_label.setText("🔍 Đang tìm người làm AI cảm nắng...")
            self.detecting = True
            QTimer.singleShot(1000, self.detect_emotion)

    def detect_emotion(self):
        try:
            results = DeepFace.analyze(self.current_frame, actions=['emotion'], enforce_detection=False)

            if not isinstance(results, list):
                results = [results]

            emotion_scores = []  # Lưu lại score của target_emotion theo từng người

            self.table.setRowCount(len(results))
            for idx, res in enumerate(results):
                score = res['emotion'].get(self.target_emotion, 0)  # Điểm cảm xúc cần thiết

                emotion_scores.append(score)

                self.table.setItem(idx, 0, QTableWidgetItem(f"Player {idx+1}"))
                self.table.setItem(idx, 1, QTableWidgetItem(f"{score:.1f}"))

            # So sánh và tìm người có score thấp nhất cho target_emotion
            if emotion_scores:
                weakest_index = emotion_scores.index(min(emotion_scores))
                self.info_label.setText(f"🙃 Người chơi {weakest_index+1} đã làm AI đổ vì biểu cảm của mình!")
            
                result = results[weakest_index]

                self.emotion_scores = result['emotion']
                self.current_emotion = result['dominant_emotion']

                face_img = result["region"]
                x, y, w, h = face_img["x"], face_img["y"], face_img["w"], face_img["h"]
                self.detected_face_image = self.current_frame
                face_crop = self.current_frame[y:y + h, x:x + w]
                face_labeled = self.draw_label_on_face(face_crop, self.current_emotion)

                qimg = QImage(face_labeled.data, face_labeled.shape[1], face_labeled.shape[0], face_labeled.strides[0], QImage.Format_RGB888)
                pix = QPixmap.fromImage(qimg)
                self.face_label.setPixmap(pix.scaled(self.face_label.size(), Qt.KeepAspectRatio))

                self.ask_suggestion()

            else:
                self.info_label.setText("😅 Chưa tìm được ai cảm nắng AI rồi.")

        except Exception as e:
            self.info_label.setText(f"⚠️ Detection Error: {str(e)}")

    def draw_label_on_face(self, img, emotion):
        color_map = {
            "happy": (241, 196, 15),
            "sad": (52, 152, 219),
            "angry": (231, 76, 60),
            "surprise": (155, 89, 182),
            "fear": (52, 73, 94),
            "disgust": (46, 204, 113),
            "neutral": (149, 165, 166)
        }
        label_color = color_map.get(emotion.lower(), (0, 0, 0))
        labeled_img = img.copy()

        # Vẽ khung viền màu theo cảm xúc
        cv2.rectangle(labeled_img, (0, 0), (labeled_img.shape[1]-1, labeled_img.shape[0]-1), label_color, thickness=4)

        # Vẽ label
        text = emotion.capitalize()
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.8
        thickness = 2
        text_size = cv2.getTextSize(text, font, scale, thickness)[0]
        text_x = 5
        text_y = text_size[1] + 10

        cv2.putText(labeled_img, text, (text_x, text_y), font, scale, label_color, thickness, lineType=cv2.LINE_AA)
        return labeled_img

    def ask_suggestion(self):
            challenges = {
                "angry": [
        "Khoanh tay trước ngực, mặt cau có, môi mím chặt.",
        "Chống nạnh, mặt nghiêng một bên, mắt nhìn trừng trừng.",
        "Giơ nắm đấm trước mặt, mặt cau lại, lông mày chau.",
        "Chỉ tay về phía trước như đang đe dọa ai đó.",
        "Hai tay đan chéo, nắm chặt, nghiến răng.",
        "Nắm tay đập nhẹ vào lòng bàn tay còn lại.",
        "Đứng chống hông, nghiêng người, mặt khinh khỉnh.",
        "Tay giật nhẹ tóc hoặc vuốt ngược tóc ra sau (kiểu giận điên người).",
        "Mặt cau có, phồng má, mắt nhìn lệch sang một bên.",
        "Bước chân về trước một bước, tay nắm thành nắm đấm, hơi khom người."
    ],
    "neutral": [
        "Đứng thẳng, hai tay xuôi tự nhiên, mặt thản nhiên.",
        "Khoanh tay, gương mặt nghiêm túc, mắt nhìn thẳng.",
        "Tay đút túi quần, mắt nhìn thẳng, gương mặt bình thản.",
        "Một tay cầm cằm, mắt nhìn xa xăm.",
        "Ngồi trên ghế, chân bắt chéo, mặt lạnh lùng.",
        "Đứng nghiêng người, tay chống nhẹ vào hông.",
        "Hai tay thả lỏng, mắt nhìn thẳng camera.",
        "Tay đan vào nhau trước bụng, mặt không cảm xúc.",
        "Một tay chống cằm, mắt nhìn nghiêng.",
        "Khoác balo/túi, đứng thẳng, ánh mắt xa xăm."
    ],
    "sad": [
        "Cúi đầu, mắt nhìn xuống, tay ôm vai hoặc tay buông thõng.",
        "Một tay che mặt, mắt buồn.",
        "Ngồi co người, tay ôm gối.",
        "Tay chống má, nhìn xa xăm, mặt buồn.",
        "Tay đặt lên ngực, mắt nhắm hờ.",
        "Hai tay chống hông, vai rũ xuống.",
        "Một tay cầm khăn giấy (hoặc tay giả làm cầm khăn), mặt sụt sùi.",
        "Tựa đầu vào tường, mắt lim dim.",
        "Hai tay ôm đầu, mặt rầu rĩ.",
        "Nằm nghiêng, một tay chống đầu, ánh mắt xa xăm."
    ],
    "happy": [
        "Hai tay giơ chữ V, cười tươi.",
        "Nhảy nhẹ lên, tay dang rộng.",
        "Một tay chống hông, tay kia giơ ngón cái 👍.",
        "Tay giơ cao vẫy chào, miệng cười lớn.",
        "Hai tay nắm thành đấm, giơ ngang ngực như “Yes!”.",
        "Một tay chống cằm, tay kia chống má, mắt cười.",
        "Đứng nghiêng người, cười toe toét.",
        "Hai tay đan vào nhau trước ngực, cười hạnh phúc.",
        "Tựa tay vào vai ai đó hoặc giả bộ có vai người bên cạnh, cười tươi.",
        "Đứng dạng chân, tay chống hông, mắt cười."
    ],
    "surprise": [
        "Miệng mở chữ O, tay ôm má.",
        "Một tay che miệng, mắt mở to.",
        "Hai tay dang ra, mặt ngạc nhiên.",
        "Tay giơ lên cao, mặt hốt hoảng.",
        "Một tay chống cằm, tay kia để ngang miệng.",
        "Nghiêng người, mắt trợn to, tay chống ngực.",
        "Hai tay chắp lại kiểu “Trời ơi tin được không?”.",
        "Một tay chống hông, tay kia chỉ lên trời, mặt bất ngờ.",
        "Cúi nhẹ người về trước, mắt mở to, tay xòe.",
        "Hai tay chống đầu, mặt hoảng hốt."
    ],
    "disgust": [
        "Một tay bịt mũi, mặt nhăn nhó.",
        "Hai tay dang ra, mặt cau có kiểu “eww”.",
        "Một tay chống cằm, mặt méo mó.",
        "Tay che miệng như muốn nôn.",
        "Tay chỉ vào thứ gì đó, mặt khó chịu.",
        "Tay chống hông, nghiêng đầu, mặt ghê tởm.",
        "Hai tay xua xua, mặt lắc đầu.",
        "Một tay đưa ra phía trước như đẩy ra xa.",
        "Tay chống ngực, mặt nhăn nhó.",
        "Mặt cau có, tay xua trước mặt như xua đuổi."
    ],
    "fear": [
        "Hai tay ôm đầu, mắt mở to.",
        "Hai tay che miệng, mặt hốt hoảng.",
        "Hai tay giơ ra chắn trước ngực như tự vệ.",
        "Một tay ôm vai, một tay đưa ra trước.",
        "Tay run run, mặt lo lắng.",
        "Ngồi co chân, tay ôm gối.",
        "Tay nắm chặt vạt áo hoặc cổ áo, mặt hoảng loạn.",
        "Mắt nhìn xung quanh, tay bấu chặt vào nhau.",
        "Một tay chỉ sang một bên, mặt hoảng hốt.",
        "Nghiêng người, tay ôm đầu, mặt sợ sệt."
    ]
            }

            # Lấy danh sách thử thách tương ứng hoặc mặc định
            suggestion_list = challenges.get(self.current_emotion)
            suggestion = random.choice(suggestion_list)

            self.suggestion_box.setText(f"🤖 Làm theo mình nhé: {suggestion} \n \nHoàn thành thử thách và ghi lại khoảnh khắc này bằng cách chụp hình màn chơi lên mxh kèm theo hashtag #9.5AISTAR #Khainhan để nhận được quà từ chương trình nhé! <3")

    def save_result(self):
        if self.current_frame is None or not self.current_emotion:
            QMessageBox.warning(self, "Warning", "No data to save.")
            return

        try:
            os.makedirs("snapshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_path = f"snapshots/face_{timestamp}.jpg"
            cv2.imwrite(img_path, cv2.cvtColor(self.detected_face_image, cv2.COLOR_RGB2BGR))

            csv_file = "results.csv"
            file_exists = os.path.isfile(csv_file)
            emotion_data = ", ".join([f"{k}:{v:.1f}%" for k, v in self.emotion_scores.items()])
            suggestion = self.suggestion_box.toPlainText()

            with open(csv_file, mode="a", newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Timestamp", "Dominant Emotion", "All Emotions", "Suggestion", "Image Path"])
                writer.writerow([timestamp, self.current_emotion, emotion_data, suggestion, img_path])

            QMessageBox.information(self, "Saved", "Màn chơi đã được lưu thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Lưu thất bại:\n{str(e)}")  

    def closeEvent(self, event):
        self.cap.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FaceGameApp()
    win.show()
    sys.exit(app.exec_())