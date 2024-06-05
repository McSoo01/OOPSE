import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import easyocr
import json

import util


class LicensePlateRecognitionSystem:
    def __init__(self, model_cfg_path, model_weights_path, class_names_path, input_dir, known_plates_file):
        self.model_cfg_path = model_cfg_path
        self.model_weights_path = model_weights_path
        self.class_names_path = class_names_path
        self.input_dir = input_dir
        self.known_plates_file = known_plates_file
        self.gate = 0
        self.reader = easyocr.Reader(['en'])

        # Load class names
        with open(self.class_names_path, 'r') as f:
            self.class_names = [j.strip() for j in f.readlines() if len(j) > 2]

        # Load model
        self.net = cv2.dnn.readNetFromDarknet(self.model_cfg_path, self.model_weights_path)

        # Load known license plates
        self.known_license_plates = self.load_known_license_plates()

    def load_known_license_plates(self):
        if os.path.exists(self.known_plates_file):
            with open(self.known_plates_file, 'r') as file:
                known_plates = json.load(file)
            return known_plates
        else:
            return []

    def save_known_license_plates(self):
        with open(self.known_plates_file, 'w') as file:
            json.dump(self.known_license_plates, file)

    def add_known_license_plate(self, license_plate):
        if license_plate not in self.known_license_plates:
            self.known_license_plates.append(license_plate)
            self.save_known_license_plates()
            print(f"License plate {license_plate} added to known list.")
        else:
            print(f"License plate {license_plate} is already in the known list.")

    def process_images(self):
        for img_name in os.listdir(self.input_dir):
            img_path = os.path.join(self.input_dir, img_name)
            img = cv2.imread(img_path)
            H, W, _ = img.shape

            # Convert image
            blob = cv2.dnn.blobFromImage(img, 1 / 255, (412, 412), (0, 0, 0), True)

            # Get detections
            self.net.setInput(blob)
            detections = util.get_outputs(self.net)

            # Bboxes, class_ids, confidences
            bboxes, class_ids, scores = self.extract_bboxes(detections, W, H)

            # Apply NMS
            bboxes, class_ids, scores = util.NMS(bboxes, class_ids, scores)

            for bbox_ in range(len(bboxes)):
                xc, yc, w, h = bboxes[bbox_]
                license_plate = img[int(yc - (h / 2)):int(yc + (h / 2)), int(xc - (w / 2)):int(xc + (w / 2)), :].copy()

                img = cv2.rectangle(img,
                                    (int(xc - (w / 2)), int(yc - (h / 2))),
                                    (int(xc + (w / 2)), int(yc + (h / 2))),
                                    (0, 255, 0),
                                    10)

                license_plate_gray = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)
                _, license_plate_thresh = cv2.threshold(license_plate_gray, 64, 255, cv2.THRESH_BINARY_INV)

                output = self.reader.readtext(license_plate_thresh)

                for out in output:
                    text_bbox, text, text_score = out
                    if text_score > 0.4:
                        print(text, text_score)

                        # Compare with known license plates
                        if text in self.known_license_plates:
                            self.gate = 1
                            print(f"Match found: {text}. Gate set to {self.gate}")

                self.display_images(img, license_plate, license_plate_gray, license_plate_thresh)

        print(f"Gate status: {self.gate}")
        if self.gate == 0:
            self.enter_pin()

    def extract_bboxes(self, detections, W, H):
        bboxes = []
        class_ids = []
        scores = []

        for detection in detections:
            bbox = detection[:4]
            xc, yc, w, h = bbox
            bbox = [int(xc * W), int(yc * H), int(w * W), int(h * H)]

            bbox_confidence = detection[4]
            class_id = np.argmax(detection[5:])
            score = np.amax(detection[5:])

            bboxes.append(bbox)
            class_ids.append(class_id)
            scores.append(score)

        return bboxes, class_ids, scores

    def display_images(self, img, license_plate, license_plate_gray, license_plate_thresh):
        plt.figure()
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        plt.figure()
        plt.imshow(cv2.cvtColor(license_plate, cv2.COLOR_BGR2RGB))

        plt.figure()
        plt.imshow(cv2.cvtColor(license_plate_gray, cv2.COLOR_BGR2RGB))

        plt.figure()
        plt.imshow(cv2.cvtColor(license_plate_thresh, cv2.COLOR_BGR2RGB))

        plt.show()

    def enter_pin(self):
        correct_pin = "1234"  # Replace with the actual correct PIN
        attempts = 3

        for attempt in range(attempts):
            pin = input("Enter PIN: ")
            if pin == correct_pin:
                print("PIN correct. Access granted.")
                return
            else:
                print(f"Incorrect PIN. You have {attempts - attempt - 1} attempts left.")
        
        print("Access denied.")


# Define constants
model_cfg_path = os.path.join('.', 'model', 'cfg', 'darknet-yolov3.cfg')
model_weights_path = os.path.join('.', 'model', 'weights', 'model.weights')
class_names_path = os.path.join('.', 'model', 'class.names')
input_dir = 'C:\\Users\\Mcsoo97\\Documents\\tablice'
known_plates_file = os.path.join('.', 'known_plates.json')

# Create an instance of the LicensePlateRecognitionSystem
lprs = LicensePlateRecognitionSystem(model_cfg_path, model_weights_path, class_names_path, input_dir, known_plates_file)

# Add a known license plate
lprs.add_known_license_plate("GKAKSF")

# Process images
lprs.process_images()
