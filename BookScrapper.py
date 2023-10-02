import mysql.connector
from bs4 import BeautifulSoup
import requests
import csv

# Send requests and parse Html
scrapper = requests.get("http://books.toscrape.com/")
soup = BeautifulSoup(scrapper.text, "html.parser")

# Extract data
titles = soup.find_all("h3")
prices = soup.find_all("p", attrs={"class": "price_color"})
stocks = soup.find_all("p", attrs={"class": "instock availability"})

# Creating a csv file
file = open("Bookscrapper.csv", "w")
writer = csv.writer(file)

writer.writerow(["Title", "Price", "Stock"])


# Establish a connection to a database
conn = mysql.connector.connect(
    host="localhost",
    username="root",
    password="",
    database="BookScrapper"
)

# Create a cursor
c = conn.cursor()

# Create a table if it doesnt Exist
c.execute('CREATE TABLE IF NOT EXISTS BOOKS2 (title TEXT, Price TEXT, Stock TEXT)')

# Insert data into a database
for title, price, stock in zip(titles, prices, stocks):
    title_text = title.text
    price_text = price.text
    stocks_text = stock.text.strip()
    c.execute('INSERT INTO BOOKS2 VALUES (%s, %s, %s)', (title_text, price_text, stocks_text))

    writer.writerow([title_text, price_text, stocks_text])
    

# Execute an SQL statement
c.execute("SELECT * FROM BOOKS2")

result = c.fetchall()

for row in result:
    print(row)

# Commit changes and close connection
conn.commit()
conn.close()

# Close csv file
file.close()





# for title, price, stock in zip(titles,prices,stocks):
#     print(title.text + " " + price.text + " " + stock.text)

# for title in titles:
#     title_text = title.text
#     print(title_text)
# for price in prices:
#     print(price.text)
# for stock in stocks:
#     print(stock.text)



