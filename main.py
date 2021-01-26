import json
import config
import datetime
import tweepy

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

target = 'Nagatani'
followers = {}
followers['users'] = []
csvdata = []

def get_followers():
    cursor = -1
    while cursor != 0:

        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AT, ATS)

        api = tweepy.API(auth, wait_on_rate_limit=True, compression=True) # wait_on_rate_limit_notify=True, 
        itr = tweepy.Cursor(api.followers_ids, id=target, cursor=cursor).pages()
        try:
            for follower_id in itr.next():
                try:
                    user = api.get_user(follower_id)
                    followers['users'].append(user._json)

                    user_str = '' + user.id_str + ',' + user.screen_name + ',' + user.name + ',' + user.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    csvdata.append(user_str)
                    print(user_str)

                except tweepy.error.TweepError as e:
                    print(e.reason)
        except ConnectionError as e:
            print(e.reason)
        
        cursor = itr.next_cursor


if __name__ == '__main__':

    get_followers()
    now = datetime.datetime.now()
    with open('out_' + now.strftime('%Y%m%d_%H%M%S') + '.json', 'w') as outfile:
        json.dump(followers, outfile, indent=4)
    with open('followers_' + now.strftime('%Y%m%d_%H%M%S') + '.csv', 'w') as outfile:
        outfile.write('\n'.join(csvdata))
