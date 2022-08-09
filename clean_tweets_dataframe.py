import pandas as pd
#import numpy as np

class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """
    def __init__(self, df:pd.DataFrame):
        self.df = df
        print(self.df.head(3))
        print('Automation in Action...!!!')
        
    def drop_unwanted_column(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop(unwanted_rows , inplace=True)
        df = df[df['polarity'] != 'polarity']
        
        return df
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        """
        
        df.drop_duplicates(inplace = True)
        
        return df
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        self.df['created_at'] = pd.to_datetime(self.df['created_at'], errors='coerce')
        #df["created_at"] = pd.to_datetime(df["created_at"])
        
        self.df = df[df['created_at'] >= '2020-12-31' ]
        
        return self.df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        #df[["a", "b"]] = df[["a", "b"]].apply(pd.to_numeric)

        df[['polarity','subjectivity','retweet_count', 'favorite_count']] =  df[['polarity','subjectivity','retweet_count', 'favorite_count']].apply(pd.to_numeric)
        
        
        
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        df = df[df['lang'] == 'en']        
        return df
  
# adding the main 
if __name__ == "__main__":
      
        df_cleaned = pd.read_csv("processed_tweet_data.csv")
        clean_tweets = Clean_Tweets(df_cleaned)
        df_cleaned = clean_tweets.drop_duplicate(df_cleaned)
        df_cleaned = clean_tweets.remove_non_english_tweets(df_cleaned)
        df_cleaned = clean_tweets.convert_to_datetime(df_cleaned)
        df_cleaned = clean_tweets.drop_unwanted_column(df_cleaned)
        df_cleaned = clean_tweets.convert_to_numbers(df_cleaned)
        #print(cleaned_df['polarity'][0:5])
    
        df_cleaned.to_csv('cleaned_twitterD_data.csv')
        print('File Successfully Saved.!!!')

        #tweet_df = tweet.get_tweet_df(save = True)