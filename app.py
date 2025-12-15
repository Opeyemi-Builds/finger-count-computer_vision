import cv2
import mediapipe as mp


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

 
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    finger_count = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            # for my Finger tips and  lower joints
            tip_ids = [8, 12, 16, 20]
            pip_ids = [6, 10, 14, 18]

    
            for tip, pip in zip(tip_ids, pip_ids):
                if landmarks[tip].y < landmarks[pip].y:
                    finger_count += 1

            
            if landmarks[4].x > landmarks[3].x:
                finger_count += 1

    
    cv2.putText(frame, f"Fingers: {finger_count}", (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 255, 0), 3)

    cv2.imshow("Finger Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
# SO HELP ME GOD PLEASE JUST WORL!!!