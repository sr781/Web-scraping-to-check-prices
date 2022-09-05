import requests
import os
from bs4 import BeautifulSoup
import smtplib
my_email = os.environ["email"]
my_password = os.environ["password"]
URL = "https://www.amazon.co.uk/all-new-echo-dot-4th-generation-smart-speaker-with-alexa-charcoal/dp/B084DWCZXZ/ref=sr_" \
      "1_1?crid=2UXQD0IH1MCVO&keywords=echo&qid=1662387106&sprefix=echo%2Caps%2C401&sr=8-1"  # Url of the item
price_threshold = 60.99  # The minimum threshold
headers = {
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}
response = requests.get(url=URL, headers=headers)
yc_webpage = response.text
soup = BeautifulSoup(yc_webpage, "html.parser")  # Website is parsed using BeautifulSoup

price_tag = soup.find(name="span", class_="a-offscreen")  # Navigates the data structure to find the price which is within the "o-offscreen" class
item_tag = soup.find(name="span", id="productTitle")
price_float = float(price_tag.getText().strip("£"))
item_name = item_tag.getText()
message = f"{item_name} now only {price_float}           {URL}"  # Creates the message which will be the item name, and the current price
message = message.encode("utf-8")  # Encodes the message so it can be sent via email
if price_float <= price_threshold:  # If the price of the item is below the threshold, this if statement is triggered
    with smtplib.SMTP("outlook.office365.com") as connection:  # Using the smtplib library to send emails using the simple mail transfer protocol
        connection.starttls()  # Encrypts connection
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=os.environ["send_email"], msg=f"Subject:Price Alert!\n\n {message}")
        print("Sending...")  # Confirms that the message is being sent
