
import json
import sys
import tweepy


words_to_remove = ['Congressman', 'Senator', 'Sen.', 'Rep', 'Sen', "Representative", "DDS", "JD", "MD", "Rep.", "Congresswoman", "Office", "Press"]

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        original_tweet = tweet.retweeted_status
        user = original_tweet.user.name
        words = user.split()
        filtered_name = ""
        for word in words:
        	word = word.replace(',', '')
        	word = word.replace('.', '')
        	if not word in words_to_remove:
        		filtered_name+=word
        		filtered_name+= ' '
        filtered_name = filtered_name[:-1]
        print(filtered_name)
        if len(filtered_name.split()) > 2:
        	filtered_name = filtered_name.split()[0] + filtered_name.split()[-1]
        id = find_govtrack_id(filtered_name)
        member = find_by_id(id)
        try:
        	data = get_useful_data(member)
        	#print(data)
        	status_update =  '@' + tweet.user.screen_name + ' ' + data['name'] + ', a ' + data['party'] + ' ' + data['type'] + ' from ' + data['district'] + ' is reachable at, '
        	status_update += 'Phone: ' + data['phone']
        	#print(status_update)
        	#print(tweet.user.screen_name)
        	res = self.api.update_status(status = status_update, in_reply_to_status_id=tweet.id_str, auto_populate_reply_metadata=True)
        except:
        	print("problem with " + filtered_name)

    def on_error(self, status):
        print("Error detected")

#searches through the json by their name and returns the govtrack id associated with them
def find_govtrack_id(name):
	file = open('legislators-current.json',)
	members_of_congress = json.load(file)
	for member in members_of_congress:
		mem_name = ''
		if len(member['name']['official_full'].split()) > 2:
			mem_name = member['name']['official_full'].split()[0] + ' ' + member['name']['official_full'].split()[len(member['name']['official_full'].split()) - 1]
		else:
			mem_name = member['name']['official_full']
		if mem_name == name:
			return member['id']['govtrack']
	file.close()

#returns the members json by their govtrack id
def find_by_id(id):
	file = open('legislators-current.json',)
	members_of_congress = json.load(file)
	for member in members_of_congress:
		if member['id']['govtrack'] == id:
			return member
	file.close()


#accepts json of user and returns dict of the useful values to tweet
def get_useful_data(member):
	data = {}
	current_term = member['terms'][len(member['terms'])- 1]
	data['name'] = member['name']['official_full']
	data['party'] = current_term['party']
	data['type'] = 'Representative' if current_term['type'] == 'rep' else 'Senator'
	data['district'] = current_term['state'] + '-' + str(current_term['district']) if data['type'] == 'Representative' else current_term['state']
	data['phone'] = current_term['phone']
	data['website'] = current_term['url']
	return data
	
	


#print(get_useful_data(find_by_id(find_govtrack_id('Abigail Spanberger'))))
#print(get_useful_data(find_by_id(find_govtrack_id('Chuck Grassley'))))

def create_api():

	file = open('auth.json')
	auth_tokens = json.load(file)
	auth = tweepy.OAuthHandler(auth_tokens['api_key'], auth_tokens['api_secret_key'])
	auth.set_access_token(auth_tokens['access_token'], auth_tokens['access_token_secret'])
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	try:
		api.verify_credentials()
		print("Authentication OK")
	except:
		print("Error during authentication")
	return api

def main():
	all435reps = '1124447266205503488'
	all100senators = '825359465826353153'
	api = create_api()
	tweets_listener = MyStreamListener(api)
	stream = tweepy.Stream(api.auth, tweets_listener)
	stream.filter(follow=[all435reps, all100senators])

main()
