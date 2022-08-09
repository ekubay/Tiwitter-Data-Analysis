import json
import pandas as pd
from textblob import TextBlob
import zipfile

def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """
    
    # tweets_data = []
    # for tweets in open(json_file,'r'):
    #     tweets_data.append(json.loads(tweets))
    
    
    # return len(tweets_data), tweets_data
    tweets_data = []
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))

    return len(tweets_data), tweets_data

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):
        
        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self)->list:
        statuses_count = [x['user']['statuses_count'] for x in self.tweets_list] 
        
        return statuses_count
    
    # this function will find and return full text of a tweet from a dataframe
    def find_full_text(self)->list:  
        try:
         text = [x['full_text'] for x in self.tweets_list]
        except KeyError:
            text = None
        return text
       
    # 
    def find_sentiments(self, text)->list:
        polarity = [TextBlob(x).polarity for x in text]
        subjectivity = [TextBlob(x).subjectivity for x in text]

        return polarity, subjectivity

    # 
    def find_created_time(self)->list:
        created_at = [t['created_at'] for x in self.tweets_list]
       
        return created_at
    
    # 
    def find_source(self)->list:
        source = [x['source'] for x in self.tweets_list]

        return source

    # 
    def find_screen_name(self)->list:
        screen_name = [x['user']['screen_name'] for x in self.tweets_list]
        
        return screen_name
    
    # 
    def find_followers_count(self)->list:
        followers_count = [x['user']['followers_count'] for x in self.tweets_list]
        
        return followers_count

    # 
    def find_friends_count(self)->list:
        friends_count = [x['user']['friends_count'] for x in self.tweets_list]
        
        return friends_count

    # 
    def is_sensitive(self)->list:
        is_sensitive = []
        for tweet in self.tweets_list:
            if 'possibly_sensitive' in tweet.keys():
                is_sensitive.append(tweet['possibly_sensitive'])
            else: is_sensitive.append(None)
            
        return is_sensitive

    # 
    def find_favourite_count(self)->list:
         favorite_count = [x.get('retweeted_status',{}).get('favorite_count',0) for x in self.tweets_list]

         return favorite_count

    # 
    def find_retweet_count(self)->list:
        retweet_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                retweet_count.append(tweet['retweeted_status']['retweet_count'])
            else: retweet_count.append(0)
    
        return retweet_count

    # 
    def find_hashtags(self)->list:
        hashtags = []
        for tw in self.tweets_list:
            hashtags.append(", ".join([hashtag_item['text'] for hashtag_item in tw['entities']['hashtags']]))
            
        return hashtags

    # 
    def find_mentions(self)->list:
        mentions = []
        for tw in self.tweets_list:
            mentions.append( ", ".join([mention['screen_name'] for mention in tw['entities']['user_mentions']]))

        return mentions

    # 
    def find_location(self)->list:
        location = []
        for tweet in self.tweets_list:
            location.append(tweet['user']['location'])
        
        return location
    
    #
    def find_lang(self)->list:
        lang = [x['lang'] for x in self.tweets_list]
        
        return lang

    #    
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text', 'subjectivity', 'polarity', 'lang', 'favorite_count', 'retweet_count',
                   'original_author', 'followers_count', 'friends_count','possibly_sensitive','hashtags', 'user_mentions', 'place']
    
        created_at = self.find_created_time()
        source = self.find_source()
        #original_text = self.find_original_text()
        full_text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(full_text)
        lang = self.find_lang()
        #status_count = self.find_statuses_count()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        followers_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, full_text, subjectivity, polarity, lang, fav_count, retweet_count, 
                   screen_name,followers_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("global_twitter_data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df(save = True) 

    # use all defined functions to generate a dataframe with the specified columns above