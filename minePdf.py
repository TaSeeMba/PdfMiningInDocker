import os
import pytesseract as pt
import cv2
import json
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


def price_product_combine(list, price , unitcost , qty):
  my_dict = {}
  arr = []
  for i in range(1, len(list)):
    try:
        my_dict["Item"] = list[0]
        my_dict["Rate"] = unitcost[0]
        my_dict["Quantity"] = qty[0]
        my_dict["Totalamount"] = price[0]
        arr.append(my_dict)
    except:
        print("Error Detected: Check if you have only 1 instead of 01 in any category.")
  return arr

""" Extracts quantities per line items on invoice """  
def extract_Qtys(qtyImg):
	qty_rate = pt.image_to_string(qtyImg)
	qty_rate = qty_rate.split("\n")
	return list(filter(None, qty_rate))

""" Extracts costs per line items on invoice """  	
def extract_Costs(costImg):
	unit_cost = pt.image_to_string(costImg)
	unit_cost = unit_cost.replace("R","")
	unit_cost = unit_cost.replace("O","0")
	unit_cost = unit_cost.replace("i","1")
	return list(filter(None, unit_cost))

""" Extracts names of products per line items on invoice """  	
def extract_NameProducts(productsImg):
    name_of_products = pt.image_to_string(productsImg)
    name_of_products = name_of_products.split("\n")
    return list(filter(None, name_of_products))

""" Extracts total price per line items on invoice """  	
def extract_TotalPrices(pricesImg):
    total_price = pt.image_to_string(pricesImg)
    total_price = total_price.replace("R", "")
    total_price = total_price.split("\n")
    return list(filter(None, total_price))

""" Extracts item price per line items on invoice """  
def extract_ItemPrices(itemPriceImg):
    products_price = pt.image_to_string(itemPriceImg)
    products_price = products_price.replace("R", "")
    products_price = products_price.replace("i", "1")
    products_price = products_price.split("\n")
    return list(filter(None, products_price))

""" Extracts info of seller on invoice """  	
def extract_SellerInfo(sellerImg):
    seller_info = pt.image_to_string(sellerImg)
    return seller_info_correct(seller_info)
	
""" Extracts info of buyer on invoice """  	
def extract_BuyerInfo(buyerImg):
    buyer_info = pt.image_to_string(buyerImg)
    buyer_info = buyer_info.split("\n")
    return list(filter(None, buyer_info))

""" Extracts account info of seller on invoice """  		
def extract_AccountInfo(accountImg):
    account_no = pt.image_to_string(accountImg)
    account_no = account_no.split("\n")
    return list(filter(None, account_no))

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
	# unit cost section
    crop_img7 = img[1600:height, 1700:1950]
    # quantity section
    crop_img8 = img[1600:height, 2200:2500]

    crop_img8 = cv2.bilateralFilter(crop_img8,9,75,75)
    crop_img8 = cv2.medianBlur(crop_img8, 3)
    crop_img7 = cv2.bilateralFilter(crop_img7,9,75,75)
    crop_img7 = cv2.medianBlur(crop_img7, 3)

    seller_info = extract_SellerInfo(crop_img)
    buyer_info = extract_BuyerInfo(crop_img2)
    account_no = extract_AccountInfo(crop_img6)
    total_price = extract_TotalPrices(crop_img3)
	
    name_of_products = extract_NameProducts(crop_img4)
    products_price = extract_ItemPrices(crop_img5)
    unit_cost = extract_Costs(crop_img7)
    qty_rate = extract_Qtys(crop_img8)

    temp = price_product_combine(name_of_products, products_price, unit_cost, qty_rate)

    print("\nCreating a JSON file in current directory . . . !!!")
    dict = {"Seller Email": seller_info[0][0], "Vat-No": seller_info[1][2], "Seller address": seller_info[1][3]
      , "Tel#": seller_info[2][2], "Buyer's Address": buyer_info[3], "Buyer's Name": account_no[1]
      , "Buyer's Account": account_no[0], "Date of purchase": account_no[3],
            "Total Price": total_price[1], "Item's Billed": temp}
    #print(dict)

    with open('result.json', 'w') as fp:
        json.dump(dict, fp)
    print("\nDeleting unnecessary File.")
    os.remove(name_of_file+"-0.png")
    print("\nAll Done. Your Json file is result.json")
    return json.dumps(dict)
