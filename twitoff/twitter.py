"""Retrieve Tweets, embeddings, and persist in the database."""
import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, User


TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'), config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'), config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)
BASILICA = basilica.Connection(config('BASILICA_KEY'))

def add_or_update_user(username):
    """Add or Update a user *and* their Tweets, error if no/private user."""
    try:
        #get user info from tweepy API
        twitter_user = TWITTER.get_user(username)
        #do a DB query to see if the twitter user already exists
        db_user = (User.query.get(twitter_user.id) or User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        #we want as many recent non-retweet/reply statuses as we can get
        #since_id will pull in the most recent tweet ID we have on file
        #this allows us to only pull in new tweets.
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False, tweet_mode='extended',
            since_id=db_user.newest_tweet_id)
        #if there are new tweets to pull in, update them here!
        #this is skipped if there are no new tweets
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            #Get embedding for tweet and store in DB
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username,e))
        raise e
    else:
        DB.session.commit()

def update_all_users():
    """Update all Tweets for all Users in the User table."""
    for user in User.query.all():
        add_or_update_user(user.name)
