from Hand_detection import HandDetector
import cv2
from tensorflow.keras.models import load_model
from Mouse_control import Mouse_control

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)
model = load_model("G:/My Drive/University/HIT/HIT product 2022 - Visual mouse/program/model/MobileNet_model.h5")
mouse_control = Mouse_control((cap.get(3), cap.get(4)), frameR=120)
instance_bonus = 50
name_gesture = ('Double_Left_mouse',
                'Left_mouse',
                'Long_press_mouse',
                'Move_mouse',
                'Right_mouse',
                'Scroll_mouse')

def main():
    while True:
        success, img_cam = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            continue

        img = cv2.flip(img_cam, 1)
        
        hands, lmList, img_draw = detector.findHands(img.copy(), draw=True, flipType=False)

        if hands:
            hands1 = hands[0]
            bbox1 = hands1['bbox']
            img_crop = img[max(0, bbox1[1]-instance_bonus):bbox1[1]+bbox1[3]+instance_bonus, 
                        max(0, bbox1[0]-instance_bonus):bbox1[0]+bbox1[2]+instance_bonus]
            center_point = lmList[0][:2]
            try:
                X = cv2.resize(img_crop, (224, 224))
                X = X.reshape((1,) + X.shape)
                X = X / 255.0
                y = model.predict(X)
                id = y.argmax(axis=1)[0]
                if max(y[0]) > 0.9:
                    mouse_control.mouse(id+1, center_point)
                cv2.putText(img_draw, name_gesture[id], (bbox1[0], bbox1[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            except Exception as e:
                print(e)
        cv2.imshow('cap', img_draw)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()