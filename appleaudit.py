[5:06 pm, 24/10/2024] Vittal: import cv2
import numpy as np

def classify_apple_color(hsv_roi):
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])

    mask_red = cv2.inRange(hsv_roi, lower_red, upper_red)
    mask_yellow = cv2.inRange(hsv_roi, lower_yellow, upper_yellow)

    mask_green = cv2.inRange(hsv_roi, lower_green, upper_green)

    if cv2.countNonZero(mask_red) > 0 or cv2.countNonZero(mask_yellow) > 0:
        return "Ripe"
    elif cv2.countNonZero(mask_green) > 0:
        return "Raw"
    else:
        return "Unknown"

def process_apple_image(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blurred_image = cv2.GaussianBlur(hsv_image, (15, 15), 0)
    gray_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)
    _, thresholded_image = cv2.threshold(gray_image, 60, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        apple_roi = hsv_image[y:y+h, x:x+w]
        apple_classification = classify_apple_color(apple_roi)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, apple_classification, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    cv2.imshow("Apple Classification", image)

def capture_camera_feed():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        process_apple_image(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if _name_ == "_main_":
    capture_camera_feed()