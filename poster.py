import oauth2 as oauth
import urllib
import urlparse
import ConfigParser
import os
import sys
#Derp

access_token_url = 'http://twitter.com/oauth/access_token'
request_token_url = "http://twitter.com/oauth/request_token"
request_uri = 'https://api.twitter.com/1/statuses/update.json'
CONFIG_FILE=".git/twitter.cfg"

class Poster(object):
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(CONFIG_FILE)
        self.consumer_key=config.get("twitter","consumer_key")
        self.consumer_secret=config.get("twitter","consumer_secret")
        self.access_key=config.get("twitter","access_key")
        self.access_secret=config.get("twitter","access_secret")
        print self.consumer_key
        print self.consumer_secret
        print self.access_key
        print self.access_secret

        """
        self.consumer_key="t858JKpBpWYlztY4YOhCw"
        self.consumer_secret="TFQGLMN9qgjVLBDhvoi5LfJzlONRyMLg1JPHMpXLpW8"
        self.access_key="51963848-G8WuGfVjGen46ndeFlF8QKgLkP3DvgGsfgf3ijQdn"
        self.access_secret="vIkGrwcHGcljkIsKSU8cO7UDFACMk1Kfwn2Z7hROWY"
        """
# Create your consumer with the proper key/secret.
        token = oauth.Token(self.access_key,self.access_secret)
        consumer = oauth.Consumer(self.consumer_key,self.consumer_secret)
        self.client = oauth.Client(consumer,token)

    def tweet(self,status):
        data = {'status':str(status)}
        resp, content = self.client.request(request_uri, 'POST', urllib.urlencode(data))
        print "Status was: "+str(resp['status'])
        if resp['status'] != "200":
            print content
        else:
            print "Things went well..."

if __name__ == "__main__":
    poster = Poster()
    print "from poster Going to tweet"
    print sys.argv[1]
    poster.tweet(sys.argv[1])
