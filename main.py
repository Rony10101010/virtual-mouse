import cv2
import numpy as np
import time
import autopy
import pyautogui

from hand_tracking_module import HandDetector


def start_mouse_control():
    cam_width, cam_height = 1280, 720
    frame_margin = 10
    smooth_factor = 7

    prev_time = 0
    prev_x, prev_y = 0, 0
    is_dragging = False
    click_cooldown = 0.6
    last_click_time = 0

    cap = cv2.VideoCapture(0)
    cap.set(3, cam_width)
    cap.set(4, cam_height)
    detector = HandDetector(detection_con=0.8, max_hands=1)
    screen_width, screen_height = autopy.screen.size()

    while True:
        success, frame = cap.read()
        if not success:
            continue

        frame = detector.find_hands(frame)
        landmarks, _ = detector.find_position(frame)

        if landmarks:
            index_x, index_y = landmarks[8][1], landmarks[8][2]
            fingers = detector.fingers_up()
            current_time = time.time()

            # Move mouse
            if fingers == [0, 1, 0, 0, 0]:
                mapped_x = np.interp(index_x, (frame_margin, cam_width - frame_margin), (screen_width, 0))
                mapped_y = np.interp(index_y, (frame_margin, cam_height - frame_margin), (0, screen_height))

                curr_x = prev_x + (mapped_x - prev_x) / smooth_factor
                curr_y = prev_y + (mapped_y - prev_y) / smooth_factor

                autopy.mouse.move(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y
                cv2.circle(frame, (index_x, index_y), 15, (255, 0, 255), cv2.FILLED)

            # Single click
            if fingers == [0, 1, 0, 0, 1] and (current_time - last_click_time) > click_cooldown:
                pyautogui.click()
                last_click_time = current_time

            # Double click
            if fingers == [0, 0, 0, 0, 1] and (current_time - last_click_time) > click_cooldown:
                pyautogui.doubleClick()
                last_click_time = current_time

            # Drag
            if fingers == [1, 1, 1, 1, 1]:
                if not is_dragging:
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
                    is_dragging = True

                mapped_x = np.interp(index_x, (frame_margin, cam_width - frame_margin), (screen_width, 0))
                mapped_y = np.interp(index_y, (frame_margin, cam_height - frame_margin), (0, screen_height))

                drag_x = prev_x + (mapped_x - prev_x) / smooth_factor
                drag_y = prev_y + (mapped_y - prev_y) / smooth_factor
                autopy.mouse.move(drag_x, drag_y)
                prev_x, prev_y = drag_x, drag_y
            elif is_dragging:
                autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
                is_dragging = False

            # Right click
            if fingers[0] == 1 and fingers[4] == 1 and all(f == 0 for f in fingers[1:4]):
                autopy.mouse.click(autopy.mouse.Button.RIGHT)

        # Show FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) != 0 else 0
        prev_time = curr_time

        cv2.putText(frame, f'FPS: {int(fps)}', (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.imshow("Virtual Mouse", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_mouse_control()
