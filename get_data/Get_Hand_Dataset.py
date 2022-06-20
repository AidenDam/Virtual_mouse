import os
import cv2
import mediapipe as mp

class HandDetector:
    """
    Finds Hands using the mediapipe library. Exports the landmarks
    in pixel format. Adds extra functionalities like finding how
    many fingers are up or the distance between two fingers. Also
    provides bounding box info of the hand found.
    """

    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, minTrackCon=0.5):
        """
        :param mode: In static mode, detection is done on each image: slower
        :param maxHands: Maximum number of hands to detect
        :param detectionCon: Minimum Detection Confidence Threshold
        :param minTrackCon: Minimum Tracking Confidence Threshold
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True, flipType=True):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                ## lmList
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                ## bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                ## draw
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (255, 0, 255), 2)
                    cv2.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
        if draw:
            return allHands, img
        else:
            return allHands

def CaptureImage(name_gesture, folder_name, instance_bonus, delay_count):
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    count = 0
    number_Image = 0
    while True:
        # Get image frame
        success, img_cam = cap.read()
        
        img = cv2.flip(img_cam, 1)
        # Find the hand and its landmarks
        hands, drawed_img = detector.findHands(img.copy(), flipType=False)  # with draw
        # hands = detector.findHands(img, draw=False)  # without draw

        if hands:
            # Hand 1
            hand1 = hands[0]
            # lmList1 = hand1["lmList"]  # List of 21 Landmark points
            bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
            centerPoint1 = hand1['center']  # center of the hand cx,cy
            # handType1 = hand1["type"]  # Handtype Left or Right

            # fingers1 = detector.fingersUp(hand1)


            #Save croped image
            if count == delay_count:
                while os.path.exists(folder_name + '/' + name_gesture + '/' + str(number_Image) + ".jpg"): number_Image += 1
                img_crop = img[bbox1[1]-instance_bonus:bbox1[1]+bbox1[3]+instance_bonus, 
                               bbox1[0]-instance_bonus:bbox1[0]+bbox1[2]+instance_bonus]
                try:
                    cv2.imwrite(folder_name + '/' + name_gesture + '/' + str(number_Image) + ".jpg", img_crop)
                    number_Image += 1
                except:
                    print("Your action is so fast!")
                count = 0
            count += 1
            
            cv2.circle(drawed_img, (centerPoint1[0], centerPoint1[1]), 8, (255, 0, 255), cv2.FILLED) # draw center point
            # if len(hands) == 2:
            #     # Hand 2
            #     hand2 = hands[1]
            #     lmList2 = hand2["lmList"]  # List of 21 Landmark points
            #     bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
            #     centerPoint2 = hand2['center']  # center of the hand cx,cy
            #     handType2 = hand2["type"]  # Hand Type "Left" or "Right"

            #     fingers2 = detector.fingersUp(hand2)
                
            #     cv2.circle(img, (centerPoint2[0], centerPoint2[1]), 8, (255, 0, 255), cv2.FILLED) # draw center point

            #     # Find Distance between two Landmarks. Could be same hand or different hands
            #     # length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)  # with draw
            #     # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw
        # Display
        cv2.imshow("Image (Press q to quit)", drawed_img)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__': 
    directory = "Move_mouse"

    parent_dir = "D:/"

    path = os.path.join(parent_dir, directory)

    try:
        os.makedirs(path, exist_ok = True)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)

    CaptureImage("Move_mouse", "D:", 50, delay_count=10)