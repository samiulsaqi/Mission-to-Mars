# Mission to Mars (Web-scraping, storing and presentation)

This project is a simple approach to scrape some parts from NASA's website regarding Mars, and later presenting it in web format as a gist rather than the actual website, which has more contents. The tools for scraping used are BeautifulSoup and Selenium (Chrome Driver), and MongoDB is used for data storing and retrieval. Finally, the scraped information is presented using Flask and pre-made Bootstrap styling.


## Scraping

The Scraping done focuses on the following four items:

- Latest news about Mars from NASA
- A featured image of Mars
- Some basic facts about Mars
- Pictures of the four hemispheres of Mars

The Scraping is done through Selenium to automate the website visit and BeautifulSoup to capture the required images, texts and facts. Overall, this is done using Python environment.

## Database Storing and Retrieval

The scraped information is stored using MongoDB, which is a NoSQL database system for storing non-indexed number. As such, it provides more flexibility in storing different types of seemingly unrelated information.
The information is later retrieved by the presentation website in a pleasant and multi-device friendly format
## Presentation

After the scraping is done and the information is stored, it is presented via Flask. Standard Bootstrap 3 features are used to present them in a multi-device (PC, Mobile) friendly format.
