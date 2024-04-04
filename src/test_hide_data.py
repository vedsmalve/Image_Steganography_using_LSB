# test_hide_data.py
import time
import pyautogui

def test_hide_data():
    # Run your main application
    # Note: Adjust the path according to your project structure
    app_path = "E:\BE_Project_Steganography\src1\main.py"
    pyautogui.press('win')
    pyautogui.write(app_path)
    pyautogui.press('enter')
    time.sleep(5)  # Adjust the sleep time based on your application's startup time

    # Test the 'Hide Data' section
    pyautogui.click(200, 150)  # Adjust the coordinates based on your application
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('space')
    pyautogui.write("_f19a2713-0ab1-4578-a5e9-100f701c9dc0.jpeg")
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('space')
    pyautogui.write("WhatsApp Image 2023-08-27 at 11.15.11.jpg")
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.write("1234567891234567")
    pyautogui.press('tab')
    pyautogui.write("1234567891234567")
    pyautogui.press('tab')
    pyautogui.press('space')
    time.sleep(10)  # Adjust the sleep time based on the time taken for hiding data
    pyautogui.alert("Hide Data test completed. Check the application output.")

if __name__ == "__main__":
    test_hide_data()
