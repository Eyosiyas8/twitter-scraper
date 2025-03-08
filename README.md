## About twitter-scraper

twitter-scraper is a tool which utilizes the twint scrapping module to scrape tweets as well as replies of tweets. You can scrape the tweets as well as the replies by first provide the username you want to scrape from on the text file named 'Document' located under Authentication folder, then you can start scraping by running the scraper file named index.py
The scraper uses both mongodb and elasticsearch as a backend (i.e. it uses mongodb as a stable db and elasticsearch for its visualization capabilities).

For keyword search, you can run index_keyword.py

### Installation Packages
cd twitter-scraper

pip3 install -r requirements.txt

If you havn't already installed pip, you can install it with the following command -> 
sudo apt install python3-pip

_Also make sure you have Google Chrome installed in your machine_

pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint

### For more information on twint

https://github.com/twintproject/twint

docker build --tag 'twitter-scraper' .
docker run twitter-scraper
docker run -rm twitter-scraper
