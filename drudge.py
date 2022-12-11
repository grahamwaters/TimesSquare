# Import the necessary libraries
import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from PIL import Image
import openai
import io
# get clip from openai
clip = openai.CLIP()


# conda install -c conda-forge nltk requests pillow openai # Install the necessary libraries
# pip install -r https://raw.githubusercontent.com/openai/openai/master/requirements.txt
# to install all dependencies for the OpenAI library
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