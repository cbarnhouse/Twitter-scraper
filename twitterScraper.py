# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 16:15:20 2018

@author: Christopher Barnhouse
"""

import time
import csv
import wordcloud
import matplotlib.pyplot as pyplot 
import folium
import os
import geopy 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from geopy.geocoders import Nominatim


browser = webdriver.Chrome()                                                                                                #specifying Chrome browser for Selenium to automate
base_url = "https://twitter.com/search?f=tweets&vertical=default&q="                                                        #url that leads to Twitter search page
search_term = input("Enter the term you'd like to search. This can be a single word, multiple words/phrase, or a hashtag: ")
query = search_term + "&src=typd"                                                                                           #Search query as it's displayed in the Twitter search url

if(search_term[0] == "#"):                                                                                                  #Formatting to make hashtags work, the hashtag is replaced by "%23" in the url
   new_search_term = "%23" + search_term[1:]
   query = new_search_term + "&src=typd"
                                                       
url = base_url + query                                                                                                      #Combined, this makes the whole URL leading to query results

browser.get(url)                                                                                                            #Open up the results page in the browser
time.sleep(1)                                                                                                               #Wait for page to laod  

body = browser.find_element_by_tag_name("body")                                                                             #Assign HTML body to variable 


                                
for _ in range(5):                                                                                                        #scroll down page x times to bring more tweets into view
        body.send_keys(Keys.PAGE_DOWN)                
        time.sleep(0.2)
 
   

actions = ActionChains(browser)                              #initialize actions variable to access Selenium actions methods


##getting tweet text##
tweets = browser.find_elements_by_class_name("tweet-text")                                                                  #Twitter's HTML specifys tweet text with the class name "tweet-text"

tweets_as_strings = []                                                                                                      #add lower-cased and split tweet text to string list, otherwise the twwets are a "WebElement" object and we can't work with that any further
for tweet in tweets:
    tweets_as_strings += tweet.text.lower().split()
    
                                                                                                                            #formatting to get rid of common punctuation
for i in range(len(tweets_as_strings)):
    tweets_as_strings[i].replace(',', '')
    tweets_as_strings[i].replace(' ,', '')
    tweets_as_strings[i].replace('.', '')
    tweets_as_strings[i].replace(' .', '')
    tweets_as_strings[i].replace('!', '')
    tweets_as_strings[i].replace('?', '')
    tweets_as_strings[i].replace('"', '')
    
##getting profile links##
username_profile_links = browser.find_elements_by_class_name("js-user-profile-link")                                        #User profile links are in this HTML class
username_profile_links_as_strings = []                                                                                      #get the link attribute from the HTML and add it to list like we did with the tweet text earlier
for name in username_profile_links:
    profile_url = name.get_attribute("href")
    #print(profile_url)
    if(profile_url is not None):                                                                                            #sometimes a NoneType(null) webelement object is returned in the previous line, so we're just ignoring those for now
        username_profile_links_as_strings += profile_url.split()

##getting location info##
locations = []                                                                                                              
for link in username_profile_links_as_strings:
    try:
        browser.get(link)                                                                                                   #open up each separate user profile link
        time.sleep(0.5)
        location = browser.find_element_by_class_name("ProfileHeaderCard-locationText")                                     #location information is found in this class in twitter's HTML
        if(location.text != ''):                                                                                            #if the user's location text isn't empty, add it to "locations" string list
            locations.append(location.text)
        #print(location.text)
    except NoSuchElementException:                                                                                          #Sometimes a profile that we're visiting has been deleted or is otherwise unavailable since the time they made the tweet, 
            pass                                                                                                            #so an exception will get thrown saying that their is no location information on the page. If that happens, we ignore it and move on to the next profile
                
        
    

##counting occurences of words in tweets## 
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',                                            #list of common stopwords and words that are not useful for the purposes of a wordcloud graph
"you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 
'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 
'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 
'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 
'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 
'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 
'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 
'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 
'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 
'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 
'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 
'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', 
"needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', 
"won't", 'wouldn', "wouldn't", "&", "it's", "-", "u", "get", "also", "much", "gpt", "i've", "know",
"people", "like", "i'm", "would", "us", "need", "rt", "want", "need", "don't", "see", "that's", 
"got", "go", "could", "even", "things", search_term]


   
dictOfTweetWords = {}

for i in range(len(tweets_as_strings)):                                                                                     #add the words from the tweets to a dictionary, keeping their frequency up to date and excluding the stopwords
     if(tweets_as_strings[i] not in dictOfTweetWords and tweets_as_strings[i] not in stopwords): 
         dictOfTweetWords[tweets_as_strings[i]] = 1
     elif(tweets_as_strings[i] in dictOfTweetWords and tweets_as_strings[i] not in stopwords):
         dictOfTweetWords[tweets_as_strings[i]] += 1


"""
##writing CSV file##           
with open("tweets.csv", "w", encoding="utf-8") as csvfile:                                                                   #write to a csv file containing each word on the 1st column and their repsective values on the 2nd column. Leaving this out for now as I don't find it useful any longer
    writer = csv.writer(csvfile)
    writer.writerow(["words", "occurences"])
    writer.writerows(dictOfTweetWords.items())
"""   

  
##Wordcloud##
wordCloud = wordcloud.WordCloud(background_color="white", width=600, height=300)                                            #generate wordcloud object
wordCloud.generate_from_frequencies(dictOfTweetWords)                                                                        #generate wordcloud from dictOfTweetWords dictionary containing word:occurences values

wordcloud_file_name = search_term + "_wordcloud.png"                                                       
wordCloud.to_file(wordcloud_file_name)                                                                                      #save to this file
                                                                                

pyplot.axis("off")                                                                                                          #turn off x/y axes
pyplot.imshow(wordCloud)                                                                                                    #display the wordcloud image in the console



##geolocation##
latitudes = []
longitudes = []

geopy.geocoders.options.default_timeout = 180
geolocator = Nominatim(user_agent="Twitter_scraper")                                                                        #initialize geolocator object using Nominatim map service
for location in locations:                           
    try:               
        geolocation = geolocator.geocode(location)                                                                          #get the latitude/longitude of each location in "locations" list
        if(geolocation is not None):                                                                                        #Twitter allows funny/bogus locations to be used in user profiles. Example: "in a galaxy far far away." Geolocator will then try to find a set of coordinates for this bogus place, usually fail, and return a NoneType(null) object back. So this line will prevent the bogus locations from being added to the long/lat lists
            print(geolocation.address)
            print(geolocation.latitude)
            print(geolocation.longitude)
            print("\n")
            latitudes.append(geolocation.latitude)                                                                          #add the latitude and longitudes to their respective lists
            longitudes.append(geolocation.longitude)
    except:
        pass
        
dict_for_counting_frequency = {}                                                                                            #add together the longitude and latitude to get a sum unique to each pair of long/lat. Each location in the world has a unique long/lat so their sum will also be unique. use this as a key, add it to the dict, and update the value (frequency of location appearance) each time that sum appears. this counts how often a tweet has come from each location
for i in range(len(latitudes)):                                                                                             #this frequency is used to determine the radius of the circle plot on the map, bigger circles indicating a larger number of tweets from that area
    if((latitudes[i]+longitudes[i]) not in dict_for_counting_frequency):
        dict_for_counting_frequency[(latitudes[i]+longitudes[i])] = 1
    elif((latitudes[i]+longitudes[i]) in dict_for_counting_frequency):
        dict_for_counting_frequency[(latitudes[i]+longitudes[i])] += 1
print(dict_for_counting_frequency)


#Follium map
folium_map = folium.Map([25.0, 0.0], zoom_start=2.5, tiles="cartodbdark_matter")                                            #initialize a world map
map_file_name = search_term + "_map.html"
folium_map.save(map_file_name)                                                                                              #save to this file

for i in range(len(latitudes)):                                                                                             #calculate radius based on frequency and plot a point for each location in the locations list
    radius = dict_for_counting_frequency[(latitudes[i] + longitudes[i])]
    marker = folium.CircleMarker([latitudes[i], longitudes[i]], radius=radius+0.5)
#marker = folium.CircleMarker(location=[40.738, -73.98])

    marker.add_to(folium_map)


folium_map.save(map_file_name)    


python_file_path = os.path.dirname(os.path.realpath(__file__))

browser.execute_script('window.open();');
browser.switch_to_window(browser.window_handles[-1])
browser.get(python_file_path + "/" + map_file_name)
time.sleep(0.5)
    
browser.execute_script('window.open();'); 
browser.switch_to_window(browser.window_handles[-1])
browser.get(python_file_path + "/" + wordcloud_file_name)
