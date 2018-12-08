import numpy as np
import cv2
import io
import time
import PyPDF2
from selenium import webdriver
from io import BytesIO
from PIL import Image
from apc_scrapping.solving_captchas_code_examples.solve_captchas_with_model import recogniser
from selenium.webdriver.chrome.options import Options
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

'''*************************************************************************************'''
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
  "download.default_directory": "/path/to/download/dir",
  "download.prompt_for_download": False,
})

filename ="captcha_code.png"

url = "Input Your Url"
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': "downloaded_file"}}
command_result = driver.execute("send_command", params)
'''*************************************************************************************'''



'''*************************************************************************************'''
def filldetails(trrn,captchatext):
    trrnfield = driver.find_element_by_name("txtTrrn")
    trrnfield.send_keys(trrn)

    captchafield = driver.find_element_by_id("txtCaptcha")
    captchafield.send_keys(captchatext)

    button = driver.find_element_by_id("btnFilter")
    button.click()
    time.sleep(1)
    text = driver.find_element_by_tag_name("body").text
    print(text)
'''*************************************************************************************'''


	
'''*************************************************************************************'''	
def getcaptcha(trrn):
    driver.get(url)

    element = driver.find_element_by_id('capImg')  # find part of the page you want image of
    location = element.location
    size = element.size
    png = driver.get_screenshot_as_png()  # saves screenshot of entire page
    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save(filename)  # saves new cropped image

    frame = cv2.imread(filename)
    lower_black = np.array([90, 90, 90], dtype="uint16")
    upper_black = np.array([255, 255, 255], dtype="uint16")
    black_mask = cv2.inRange(frame, lower_black, upper_black)

    width = 72 * 4
    height = 24 * 4
    dim = (width, height)

    b = 15  # brightness
    c = 5  # contrast
    resized = cv2.resize(black_mask, dim, b - c)

    cv2.imwrite(filename,resized)
    time.sleep(1)
    captchatext = recogniser(filename)
    filldetails(trrn, captchatext)
'''*************************************************************************************'''


'''*************************************************************************************'''
def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text
'''*************************************************************************************'''



'''*************************************************************************************'''
def fetchtrrn():
    Tk().withdraw()
    filename = askopenfilename()
    text = extract_text_from_pdf(filename)

    leng = len(text)
    i = 0

    while leng != 0:
        if text[i] == 'T' and text[i + 1] == 'R' and text[i + 2] == 'R' and text[i + 3] == 'N':
            return text[((i + 3) + 11):((i + 3) + 24)]
        i += 1
        leng -= 1
'''*************************************************************************************'''


if __name__ == '__main__':
    trrn = fetchtrrn()
    print(trrn)
    getcaptcha(trrn)
