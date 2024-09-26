import psutil
import pyautogui
import pygetwindow as gw

# Tìm tiến trình Telegram
for proc in psutil.process_iter(['pid', 'name']):
    if "iMe" in proc.info['name']:
        print(f"Telegram process found: {proc.info}")


# Tìm cửa sổ Telegram
telegram_window = gw.getWindowsWithTitle("iMe")

if telegram_window:
    # Lấy cửa sổ đầu tiên tìm thấy (nếu có nhiều cửa sổ)
    window = telegram_window[0]

    # Kích hoạt cửa sổ (đưa cửa sổ lên phía trước)
    window.activate()

    # Lấy tọa độ và kích thước của cửa sổ
    x, y, width, height = window.left, window.top, window.width, window.height

    # Chụp ảnh màn hình chỉ trong khu vực cửa sổ đó
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    # Lưu ảnh chụp màn hình
    screenshot.save("screenshot_telegram_window.png")

    print(f"Screenshot of {window.title} saved!")
else:
    print("No Telegram window found.")
