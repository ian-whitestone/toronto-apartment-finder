import slacker
import pprint

pp = pprint.PrettyPrinter(indent=4)

token = 'xoxp-123278590487-122675302309-122711911733-f6553232998b1104ec16f10678b10329'
bot = slacker.Slacker(token)

channels_response=bot.channels.list()

channel_dict={chan['name']:chan['id'] for chan in channels_response.body['channels']}
#get channel id
channel_id=channel_dict['housing']

print (channel_dict)

response=bot.channels.history(channel_id)

##need to get file id of messages

# print ('\n \n \n')
# for r in response:
    # pp.pprint(r)
