# TimesSquare
Using CLIP and Sentiment of Drudge, and other sources, for Generative Art.

Import the necessary libraries for this project, including the requests library for downloading the HTML file and the NLTK library for sentiment analysis.

Define a function for downloading the HTML file from the Drudge website. This function should take the URL of the website as an input and return the HTML content as a string.

Define a class for the Drudge website data. This class should have attributes for the HTML content, a list of article titles, and a list of article sentiments (calculated using NLTK).

Define a method in the Drudge class for parsing the HTML content and extracting the article titles. This method should store the titles in the appropriate attribute of the class.

Define a method in the Drudge class for calculating the sentiment of each article title using NLTK. This method should store the sentiments in the appropriate attribute of the class.

Define a method in the Drudge class for generating the waffle chart. This method should take the size of the chart as an input and use the sentiments of the articles to color each square in the chart.

Create an instance of the Drudge class and download the HTML content from the website.
Use the methods of the class to parse the HTML, calculate the sentiments of the articles, and generate the waffle chart.

Display the waffle chart using a plotting library such as matplotlib.

```python
# Import the necessary libraries
import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from PIL import Image
from openai import CLIP

# Define a function for downloading the HTML file from the Drudge website
def download_html(url):
    response = requests.get(url)
    return response.text

# Define a class for the Drudge website data
class Drudge:
    def __init__(self, html):
        self.html = html
        self.titles = []
        self.sentiments = []

    # Define a method for parsing the HTML content and extracting the article titles
    def parse_html(self):
        start_index = self.html.find("<h2>")
        while start_index != -1:
            end_index = self.html.find("</h2>", start_index)
            title = self.html[start_index + 4:end_index]
            self.titles.append(title)
            start_index = self.html.find("<h2>", end_index)

    # Define a method for calculating the sentiment of each article title
    def calculate_sentiments(self):
        nltk.download("vader_lexicon")
        analyzer = SentimentIntensityAnalyzer()
        for title in self.titles:
            sentiment = analyzer.polarity_scores(title)
            self.sentiments.append(sentiment["compound"])

    # Define a method for generating the waffle chart
    def generate_waffle_chart(self, size):
        image_data = clip.generate(
            model="image-alpha-001",
            size=size,
            input_type="random"
        )
        image = Image.open(io.BytesIO(image_data))
        pixels = image.load()
        width, height = image.size
        for x in range(width):
            for y in range(height):
                r, g, b, a = pixels[x, y]
                if a == 0:
                    continue
                sentiment = self.sentiments[x]
                if sentiment > 0:
                    pixels[x, y] = (0, 255, 0)
                elif sentiment < 0:
                    pixels[x, y] = (255, 0, 0)
                else:
                    pixels[x, y] = (0, 0, 255)
        return image

# Create an instance of the Drudge class and download the HTML content from the website
url = "https://www.drudgereport.com/"
html = download_html(url)

# Use the methods of the class to parse the HTML, calculate the sentiments of the articles, and generate the waffle chart
drudge = Drudge(html)
drudge.parse_html()
drudge.calculate_sentiments()
image = drudge.generate_waffle_chart(100)

# Display the waffle chart
image.show()
```
