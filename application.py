from flask import Flask, render_template, request
from flask_cors import cross_origin
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

application = Flask(__name__) # initializing a flask app
app=application

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            url = request.form['content'].replace(" ","")
            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            pw_url = driver.get(url)
            html_content = driver.page_source
            soup = bs(html_content, 'html.parser')
            d = soup.find_all('a',{"class" , "yt-simple-endpoint inline-block style-scope ytd-thumbnail"})
            del d[0]
            links = []
            for i in range(5):
                links.append('https://www.youtube.com' + d[i]['href'])
            reviews = []
            def details(l):
                for i in l:
                    response = requests.get(i)
                    soup = bs(response.text, "html.parser")
                    title = soup.find("meta", itemprop="name")['content']
                    views = soup.find("meta", itemprop="interactionCount")['content']
                    date = soup.find("meta", itemprop="uploadDate")['content']
                    thumb = soup.find("link", itemprop="thumbnailUrl")['href']
                    review = {'Title': title, 'Url':i, 'Date Posted': date, 'Views': views, 'Thumbnail Url':thumb}
                    reviews.append(review)
            details(links)
            driver.close()
            return render_template('results.html', reviews=reviews[0:(len(reviews))])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
     app.run()
