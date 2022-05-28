import tkinter as tk

import matplotlib.pyplot
import numpy as np
from PIL import Image, ImageTk
import cv2
from matplotlib import pyplot as plt
from pystac_client import Client
import requests

api_url = "https://earth-search.aws.element84.com/v0"

root = tk.Tk()

canvas = tk.Canvas(root, height=700, width=800)
canvas.pack()




def GetImage():

    print("getting satellite imagery")

    client = Client.open(api_url)
    collection = "sentinel-s2-l2a-cogs"

    # AMS coordinates
    lat, lon = 34.0522, 118.2437 #can be changed, alter coordinates for specific location
    geometry = {"type": "Point", "coordinates": (lon, lat)}

    mysearch = client.search(
        collections=[collection],
        intersects=geometry,
        max_items=10,
    )
    print(mysearch.matched())
    items = mysearch.get_all_items()

    assets = items[-1].assets #retrieves last item from dictionary
    print(assets.keys())
    URL = assets["thumbnail"].href

    response = requests.get(URL)
    open("SatelliteImage.png", "wb").write(response.content) #downloads the current satellite image


GetImage()





img0 = cv2.imread('SatelliteImage.png')

gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY) #converts image to black and white to highlight contrast between road and terrain
img = cv2.GaussianBlur(gray, (3, 3), 0)

laplacian = cv2.Laplacian(img, cv2.CV_64F)
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)  # x 
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)  # y

plt.figure(figsize=(64, 64))
plt.subplot(1, 1, 1), plt.imshow(sobelx, cmap='gray')
plt.title(''), plt.xticks([]), plt.yticks([])

plt.savefig('NewMapImage.png')



print("loading new satellite imagery")
NewImage = (Image.open("NewMapImage.png"))

#cropping image to get specific section
w, h = NewImage.size

left = w/5
right = 7*w/9
upper = h/6
lower = (3*h)/4

NewImage2 = NewImage.crop([left,upper,right,lower])
ResizedImage = ImageTk.PhotoImage(NewImage2.resize((600,600)))

#FinalImage = ImageTk.PhotoImage(ResizedImage)

label1 = tk.Label(root, image=ResizedImage)
label1.place(x=0, y=0, relwidth=1, relheight=1)



Button = tk.Button(root, height= 10, width= 50, text="Click to show original satellite imagery")

Button.pack()



root.mainloop()
