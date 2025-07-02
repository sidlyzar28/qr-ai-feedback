import cv2

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        print("QR Code Data:", data)
        break
    cv2.imshow("QR Scanner", img)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
