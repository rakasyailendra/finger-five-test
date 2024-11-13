import cv2
import mediapipe as mp

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Fungsi untuk menghitung jumlah jari yang diangkat
def count_fingers(hand_landmarks):
    tips_ids = [mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.PINKY_TIP]
    
    fingers = []

    # Ibu jari
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Empat jari lainnya
    for tip_id in tips_ids:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

# Buka kamera eksternal (ganti 1 dengan ID kamera eksternal jika diperlukan)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Gagal menangkap gambar.")
        break

    # Konversi gambar ke format RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Deteksi tangan
    results = hands.process(image)

    # Kembali ke format BGR untuk ditampilkan dengan OpenCV
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Gambar tanda tangan
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            )

            # Hitung jumlah jari yang diangkat
            fingers_up = count_fingers(hand_landmarks)

            # Tentukan label tangan (kanan atau kiri) menggunakan multi_handedness
            hand_label = "Tangan Tidak Diketahui"
            if results.multi_handedness:
                handedness = results.multi_handedness[idx].classification[0].label
                if handedness == "Right":
                    hand_label = "Tangan Kanan"
                elif handedness == "Left":
                    hand_label = "Tangan Kiri"

            # Tampilkan jumlah jari yang diangkat dengan label tangan
            cv2.rectangle(image, (10, 10), (350, 80), (0, 0, 0), -1)  # Background hitam untuk teks
            cv2.putText(image, f'{hand_label}: {fingers_up} jari diangkat', (15, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Tampilkan gambar
    cv2.imshow('Deteksi Tangan', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

