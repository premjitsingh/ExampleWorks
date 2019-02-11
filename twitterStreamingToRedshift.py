from tweepy import StreamListener,Stream,OAuthHandler
import boto3
import logging

class TweetListener(StreamListener):

    def on_data(self,data):
        firehose_client = boto3.client('firehose',
                                        aws_access_key_id='<aws_access_key_id created obove>',
                                        aws_secret_access_key='<aws_secret_access_key created above>'
                                       )
        try:
            print "putting data"
            response = firehose_client.put_record(DeliveryStreamName='twitter_feed_to_rs',
                                                  Record={
                                                           'Data': data
                                                         }
                                                  )
            logging.info(response)
            return True
        except Exception:
            logging.exception("Problem pushing to firehose")

    def on_error(self, status):
        print status

auth=OAuthHandler('consumer_key', 'consumer_secret')
auth.set_access_token('access_token_key', 'access_token_secret')

twitter_stream = Stream(auth, TweetListener())
twitter_stream.filter(track=["donald"])