import cv2
import mediapipe as mp
import numpy as np

# Function to calculate the area of a polygon using the shoelace formula
def calculate_area(vertices):
    n = len(vertices)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    area = abs(area) / 2.0
    return area

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Load a sample image or capture video from a webcam
image = cv2.imread('hand_image.jpg')  # Replace with your own image path or use cv2.VideoCapture() for video

# Convert the image to RGB and process it with MediaPipe
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
with mp_hands.Hands(static_image_mode=True, max_num_hands=1) as hands:
    results = hands.process(image_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the landmarks' coordinates
            landmarks = []
            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                landmarks.append((x, y))
            
            # Apply convex hull algorithm to get the hand region polygon
            hull = cv2.convexHull(np.array(landmarks))
            
            # Calculate the area of the hand region
            area = calculate_area(hull)
            
            # Draw the hand region and display the area
            cv2.drawContours(image, [hull], 0, (0, 255, 0), 2)
            cv2.putText(image, f"Area: {area}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            
# Display the image with hand region and area
cv2.imshow("Hand Area", image)
cv2.waitKey(0)
cv2.destroyAllWindows()