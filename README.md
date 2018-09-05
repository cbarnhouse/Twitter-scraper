# Twitter-scraper
The Twitter scraper takes in a string as input from the user and automates a browser to search “Twitter.com/search” for all tweets containing the search string, identifies and collects all of the words in the tweets through HTML class lookup and counts each word’s frequency. Then it navigates to every user’s profile who made the tweets and collects their publicly displayed location information, uses Nominatim to lookup a latitude/longitude for every location, and counts frequency. Once all data is collected and counted, a global map is rendered with a plot point on every location that a tweet was derived from, with the radius of the plot based on the frequency of the location (a bigger circle for more frequent locations), and a “word cloud” graph is made based on the word frequencies. One of my largest executions of the program collected 30,591 words from 1,934 users located in 420 unique locations across the globe! 

The map html, graph, and images of the map for my largest execution are included in this repository under the "9-3-18-#space" folder. #space is the hashtag I searched for.

# Libraries 
I use Selenium to automate the browser, make the search, and collect the tweet/location text. Folium is used to create the map. wordcloud is used to create the wordcloud. Matplotlib is used to display the wordcloud. Geopy is used for location lookup. 
