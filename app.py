from bs4 import BeautifulSoup as bs 
import requests 
from PIL import Image
import os
import shutil

SAVE_FOLDER = 'images'
SAVE_FOLDER_IMAGE = 'pdfs'

slideshare_URL = 'https://fr.slideshare.net/kortriadh/rapport-pfe-dveloppement-dune-application-de-gestion-des-cartes-de-fidlitstaggisttunis-32571204'

if not os.path.exists(SAVE_FOLDER_IMAGE):
       os.mkdir(SAVE_FOLDER)
else:
       shutil.rmtree("./images")
       os.mkdir(SAVE_FOLDER)

if not os.path.exists(SAVE_FOLDER_IMAGE):
       os.mkdir(SAVE_FOLDER_IMAGE)

def saveImagesFromScribed():
       print("Extracting pages from SlideSgare ...")

       usr_agent = {
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive',
       }

       # load the projectpro webpage content 
       r = requests.get(slideshare_URL, headers=usr_agent) 

       # convert to beautiful soup 
       soup = bs(r.content, "html.parser")

       # # printing our web page 
       # print(soup.prettify()) 

       # Getting image URL
       results = soup.find_all('a', {'class': 'SlideContainer_documentSlide__2vQMc'})

       # Save all pages found
       for  index, result in enumerate(results):

              images = result.select('div source') 
              
              # Extract the exact Image url of the page
              images_url = images[0]['srcset'].split()[4]

              # Download the image
              img_data = requests.get(images_url).content 

              with open('images/page' + str(index + 1) + '.jpg', 'wb') as handler: 
                     handler.write(img_data) 

def listAllFiles(path="./"):
       return os.listdir(path)

def convertImagesToPdfs(pdfName="pdf"):
       print("Preparing PDF file ...")

       images = listAllFiles("./images")

       image_list = []
       
       for image in images:
              image_list.append(Image.open(r'./images/' + image).convert('RGB'))
       img = image_list.pop(0)
       img.save(r'./pdfs/' + pdfName + '.pdf', save_all=True, append_images=image_list)

saveImagesFromScribed()
convertImagesToPdfs("rapport-pfe-dveloppement-dune-application-de-gestion-des-cartes")
print("Done")