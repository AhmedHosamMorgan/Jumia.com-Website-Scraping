import csv
import requests
from bs4 import BeautifulSoup

print ("Jumia Mobile Phone Products By Price. ")
Price = input ("Enter The Range of Prices You Want In This Formatting *****-***** : ")
page = requests.get(f"https://www.jumia.com.eg/phones-tablets/?price={Price}#catalog-listing")
#
def main(page):

    src = page.content
    soup = BeautifulSoup(src, "lxml")
    Products_Details = []

    Products = soup.find("div", class_="-paxs row _no-g _4cl-3cm-shs")
    Product = Products.find_all("article", class_="prd _fb col c-prd")
    Numbers_of_Products = len(Product)

    for i in range(Numbers_of_Products):

        # Get Product Name
        Product_Name = Product[i].find("h3").text.strip()
        #print (Product_Name)

        # Get Price
        Product_Price = Product[i].find("div", class_="prc").text
        # print(Product_Price)

        # Get Old Price
        Old_Price_Tag = Product[i].find("div", class_="old")
        Old_Price = Old_Price_Tag.text if Old_Price_Tag else "0"
        # print (Old_Price)

        # Get Discount Percentage
        Discount_Tag = Product[i].find("div", class_="bdg _dsct _sm")
        Discount = Discount_Tag.text if Discount_Tag else "0"
        # print (Discount)


        Products_Details.append({
            "Product_Name": Product_Name,
            "Product_Price": Product_Price,
            "Old_Price": Old_Price,
            "Discount": Discount
        })

    return Products_Details

# Save The Result In CSV
products_data = main(page)

with open('Jumia.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
    fieldnames = ["Product_Name", "Product_Price", "Old_Price", "Discount"]
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products_data)
    print("Jumia.csv File Created.")
