from wit import Wit
from pprint import pprint

access_token = "LJBITS2IOGPLPDTVH5YYDSW2OTCD6YKZ"
client = Wit(access_token = access_token)

def wit_response(message_text):
	resp = client.message(message_text)

	entities = []
	try:
		for i in range(len(list(resp['entities']))):
			print(i)
			entity= list(resp['entities'])[i]
			value= resp['entities'][entity][0]['value']
			entities.append({
				"name":entity,
				"value":value
			})
	except:
		pass

	return entities

# pprint(wit_response("remind me with harbana menha"))
