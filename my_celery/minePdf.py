import os
import pytesseract as pt
import cv2
from wand.image import Image
from wand.color import Color


def convert_pdf(filename, output_path, resolution=150):
    """ Convert a PDF into images.

        All the pages will give a single png file with format:
        {pdf_filename}-{page_number}.png

        The function removes the alpha channel from the image and
        replace it with a white background.
    """
    print("Converting "+filename+" into Image!!\nPlease Wait. . .")

    all_pages = Image(filename=filename, resolution=resolution)
    for i, page in enumerate(all_pages.sequence):
        with Image(page) as img:
            img.format = 'png'
            img.background_color = Color('black')
            #img.alpha_channel = 'remove'

            image_filename = os.path.splitext(os.path.basename(filename))[0]
            image_filename = '{}-{}.png'.format(image_filename, i)
            image_filename = os.path.join(output_path, image_filename)
            img.save(filename=image_filename)

def RepresentsInt(s):
  try:
    int(s)
    return True
  except ValueError:
    return False


def seller_info_correct(seller_info):
  seller_info = seller_info.split("\n")
  seller_info[0] = seller_info[0].split(" ", 1)
  seller_info[2] = seller_info[2].split(" ")
  seller_info[1] = seller_info[1].split(" ", 3)
  return seller_info


def price_product_combine(list, price):
  my_dict = {}
  for i in range(1, len(list)):
    my_dict[list[i]] = price[i]
  return my_dict


def extractText(name_of_file):
    print("\nReading Image's text. . .")
    imgname = name_of_file + "-0.png"
    img = cv2.imread(imgname)
    height, width, channel = img.shape
    # seller section
    crop_img = img[350:1000, 1600:3000]
    # buyer section
    crop_img2 = img[1000:1600, 300:1100]
    # account number section
    crop_img6 = img[1000:1600, 1100:1700]
    # total price section
    crop_img3 = img[1000:1600, 1800:2900]
    # product names section
    crop_img4 = img[1600:height, 500:1200]
    # product price section
    crop_img5 = img[1600:height, 2500:2900]

    seller_info = pt.image_to_string(crop_img)
    seller_info = seller_info_correct(seller_info)
    buyer_info = pt.image_to_string(crop_img2)
    buyer_info = buyer_info.split("\n")
    buyer_info = list(filter(None, buyer_info))
    account_no = pt.image_to_string(crop_img6)
    account_no = account_no.split("\n")
    account_no = list(filter(None, account_no))
    total_price = pt.image_to_string(crop_img3)
    total_price = total_price.replace("R", "")
    total_price = total_price.split("\n")
    total_price = list(filter(None, total_price))
    name_of_products = pt.image_to_string(crop_img4)
    name_of_products = name_of_products.split("\n")
    name_of_products = list(filter(None, name_of_products))
    products_price = pt.image_to_string(crop_img5)
    products_price = products_price.replace("R", "")
    products_price = products_price.replace("i", "1")
    products_price = products_price.split("\n")
    products_price = list(filter(None, products_price))
    temp = price_product_combine(name_of_products, products_price)
    print("\nCreating a JSON file in current directory . . . !!!")
    dict = {"Seller Email": seller_info[0][0], "Vat-No": seller_info[1][2], "Seller address": seller_info[1][3]
      , "Tel#": seller_info[2][2], "Buyer's Address": buyer_info[3], "Buyer's Name": account_no[1]
      , "Buyer's Account": account_no[0], "Date of purchase": account_no[3],
            "Total Price": total_price[1], "Item's Billed": temp}
    #print(dict)
    import json
    with open('result.json', 'w') as fp:
        json.dump(dict, fp)
    print("\nDeleting unnecessary File.")
    os.remove(name_of_file+"-0.png")
    print("\nAll Done. Your Json file is result.json")
    return json.dumps(dict)
