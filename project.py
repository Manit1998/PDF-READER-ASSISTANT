import keyboard
import speech_recognition as sr
from wand.image import Image
from PIL import Image as PI
import io
req_image = []
final_text = []

from pytesseract import image_to_string
import pytesseract

import pyttsx3
eng = pyttsx3.init()
volume = eng.getProperty('volume')
eng.setProperty('volume', volume-0.00)
rate = eng.getProperty('rate')
eng.setProperty('rate', 135)

image_pdf = Image(filename="ocr.pdf", resolution=300)
image_jpeg = image_pdf.convert('jpg')

# image_jpeg = image_jpeg.convert('L')

for img in image_jpeg.sequence:
    # img = img.convert('L')
    img_page = Image(image=img)
    req_image.append(img_page.make_blob('jpg'))

# for img in req_image:
#     # txt = tool.image_to_string(
#     #     PI.open(io.BytesIO(img)),
#     #     lang=lang,
#     #     builder=pyocr.builders.TextBuilder())
#     output = pytesseract.image_to_string(PI.open(io.BytesIO(img)))
#     print (output)

while(True):
    r = sr.Recognizer()
    r.dynamic_energy_thresold = False
    old = False
    print(sr.Microphone.list_microphone_names())

    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    print("fetching")
    try:
        input1 = r.recognize_google(audio)
        print("You said: " + input1)
        if(input1 == "down"):
            keyboard.press_and_release('Page Down')
        if(input1 == "up"):
            keyboard.press_and_release('Page Up')
        if(input1=="zoom in page"):
            keyboard.press_and_release('Ctrl + =')
        if(input1=="zoom out page"):
            keyboard.press_and_release('Ctrl + -')
        if(input1 == "read the PDF"):
            for img in req_image:
                output = pytesseract.image_to_string(PI.open(io.BytesIO(img)))
                print (output)
                eng.say(output)
                eng.runAndWait()

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        continue
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))
        continue
# keyboard.press_and_release('m')

# keyboard.wait('Ctrl')
