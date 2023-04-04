import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.zillow.com/homes/'

# create a list of URLs for the three categories: sale, rent, and sold
category_urls = [url + 'for_sale/', url + 'for_rent/', url + 'recently_sold/']

# create an empty list to store the data
data = []

# loop through each category URL
for category_url in category_urls:

    # loop through each page of the category
    for page in range(1, 101):  # assuming there are 100 pages maximum
        # create the page URL
        page_url = category_url + str(page) + '_p/'

        # request the page content
        response = requests.get(page_url)

        # check if the request was successful
        if response.status_code == 200:
            # parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # find all the home listings on the page
            listings = soup.find_all('article', {'class': 'list-card'})

            # loop through each home listing
            for listing in listings:
                # extract the category (sale/rent/sold)
                category = listing.find('div', {'class': 'list-card-status'}).text.strip()

                # extract the house features
                features = listing.find('ul', {'class': 'list-card-details'}).text.strip()

                # extract the address
                address = listing.find('address', {'class': 'list-card-addr'}).text.strip()

                # extract the state
                state = address.split(',')[1].strip().split(' ')[0]

                # extract the zip code
                zip_code = address.split(',')[2].strip().split(' ')[1]

                # extract the price
                price = listing.find('div', {'class': 'list-card-price'}).text.strip()

                # extract the open time/posting time
                open_time = listing.find('div', {'class': 'list-card-status'}).find('div').text.strip()

                # append the data to the list
                data.append([category, features, address, state, zip_code, price, open_time])

        # if the request was not successful, print an error message
        else:
            print(f'Error: {response.status_code}')

# save the data to a CSV file
with open('zillow_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Category', 'House Features', 'Address', 'State', 'Zip Code', 'Price', 'Open Time/Posting Time'])
    for row in data:
        writer.writerow(row)
