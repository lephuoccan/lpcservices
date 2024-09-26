import cv2
import numpy as np
import pyautogui

# Chụp màn hình
screenshot = pyautogui.screenshot()
image = np.array(screenshot)

# Chuyển đổi ảnh màn hình sang không gian màu HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Thiết lập phạm vi Hue từ 50 đến 75
lower_hue = np.array([30, 0, 0])  # H = 50, S >= 50, V >= 50 (đảm bảo không lấy vùng quá tối)
upper_hue = np.array([100, 255, 255])  # H = 75, S và V tối đa

# Tạo mặt nạ giữ lại các vùng màu có Hue từ 50 đến 75
mask = cv2.inRange(hsv_image, lower_hue, upper_hue)

# Áp dụng mặt nạ lên ảnh gốc để giữ lại các vùng có màu mong muốn
filtered_image = cv2.bitwise_and(image, image, mask=mask)

# Chuyển ảnh đã lọc sang grayscale để tìm kiếm đối tượng
gray_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)

# Đọc các ảnh mẫu với kích thước khác nhau
templates = [
    cv2.imread('items/gold2.PNG', 0),
    cv2.imread('items/gold3.PNG', 0),
    cv2.imread('items/gold4.PNG', 0),
    cv2.imread('items/box1.PNG', 0)
]

# Ngưỡng phát hiện
threshold = 0.8

# Duyệt qua từng template và tìm kiếm
for template in templates:
    w, h = template.shape[::-1]
    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    
    # Vẽ khung quanh các đối tượng được tìm thấy
    for pt in zip(*loc[::-1]):
        cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

# Hiển thị ảnh kết quả
cv2.imshow("Detected Objects with Hue 50 to 75", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
