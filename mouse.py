import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Couldn't access the camera.")
    exit()

cv2.namedWindow('Virtual Mouse', cv2.WINDOW_NORMAL)  # Create a resizable window
cv2.setWindowProperty('Virtual Mouse', cv2.WND_PROP_TOPMOST, 1)  # Set window to be always on top

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            for landmark_id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if landmark_id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=15, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    pyautogui.moveTo(index_x, index_y)
                
                if landmark_id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=15, color=(255, 230, 0))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                
                    if abs(index_y - thumb_y) < 15:
                        pyautogui.click()
                        pyautogui.sleep(1)

                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)
    
    cv2.imshow('Virtual Mouse', frame)
    cv2.moveWindow('Virtual Mouse', screen_width - frame_width, screen_height - frame_height)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
