import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import sound
import time

# Define focal length and known object widths (in cm)
focal = 1500  # Example focal length, adjust as needed
known_widths = {
    'person': 45,  # Average width of a person in cm
    'car': 200,    # Average width of a car in cm
    'bicycle': 60, 
    'bus': 230,  
    'truck': 230,
    'cell phone':5,
    'chair': 55,
    'couch':75,
    'bed':100,
    'dining table':65,
    'tv':65,
    'refrigerator':60,
    'sink':50,
    'microwave':45,
    'umbrella':50,
    'clock':15
}

# Function to calculate distance from camera
def get_distance(pixels, known_width):
    return (known_width * focal) / pixels

# Function to vibrate multiple times
def warning_multiple_times(times, duration):
    for _ in range(times):
        sound.play_effect('digital:ZapThreeToneUp')
        time.sleep(duration)

# Create video capture object
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    bbox, label, conf = cv.detect_common_objects(frame, confidence = 0.1, nms_thresh=0.1, model ='yolov3-tiny')

    # Calculate and display distance for detected objects
    for i, lbl in enumerate(label):
        if lbl in known_widths:
            x, y, w, h = bbox[i]
            object_width_pixels = w - x
            distance = get_distance(object_width_pixels, known_widths[lbl])
            cv2.putText(frame, f'{lbl} {int(distance)} cm', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if distance < 50:
                cv2.putText(frame, 'WARNING: Object too close!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                warning_multiple_times(3, 0.5)  # Vibrate 3 times with 0.5 seconds pause


    # Draw bounding boxes and labels on the frame
    output_image = draw_bbox(frame, bbox, label, conf)

    # Display the output frame
    cv2.imshow("Object Detection and Distance Measurement", output_image)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close windows
cap.release()
cv2.destroyAllWindows()
