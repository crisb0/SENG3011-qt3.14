#usr/bin/env python3
from flask import Flask
from flask_restful import Api, Resource, abort
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser 
import re

# import fncs from files
from other import get_asx_list

app = Flask(__name__)
api = Api(app)


class Company(Resource):
	asx_dict = get_asx_list()
	print asx_dict.keys()

	################################
	#### GET FACEBOOK ID		####
	#### input: query string	####
	#### return: fb page ID		####
	################################
	def getFacebookID(self, name):
		# name can be provided as ASX ticker code (WOW.ASX) OR company name (Woolworths)	
		# if ticker code (regex ***.ASX: look through dict
		company_name = name		
		try:
			match = re.match(r'([A-Za-z]{3})\.ASX', name).group(1)
			if match is not None and match in self.asx_dict:
				company_name = self.asx_dict[match]
				print company_name
				company_name = re.sub('\sLIMITED','',company_name) # remove LIMITED bc it doesn't return results usually
				print company_name
		except:
			pass	
		return company_name
					
			
		# use https://graph.facebook.com/v2.12/search?q=<COMPANYNAME>&type=page

	args = {
        'start_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
        'end_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
		'stats': fields.DelimitedList(fields.Str(), required=False),
				# example usage: "/?stats=id,name,website,description"
				# stats can include id, name, website, description, category, fan_count, post_type, post_message, post_created_time, post_like_count, post_comment_count
			}
	@use_kwargs(args)
	####################################
	#### GET						####
	#### INPUT: queries from args	####
	#### RETURN: json output		####
	####################################
	# GET must return json output with: PageId, InstrumentIDs, CompanyNames, PageName, Website, Description, Category, fan_count, posts[id, type, message, created_time, like_count, comment_count]
	def get(self, name, start_time, end_time, stats):
		page_id = self.getFacebookID(str(name));
		print stats;
		for x in stats:
			print x;
			# SEARCH FOR INTERESTED STATISTICS HERE
		print page_id;
		return {"name": name,
				"start":str(start_time),
				"end": str(end_time),
				"PageID": page_id,
				"InstrumentIDs":'',
				"CompanyNames":'',
				"PageName":'',
				"Website":'',
				"Description":'',
				"Category":'',
				"fan_count":'',
				"posts":{
					"hello":'',
					
				}



		}
		

@app.route('/')
def index():
    return "TtESTESTEST QT314!"


@parser.error_handler
def handle_error(err):
    abort(422, errors=err.messages) # 422 Unprocessable Entity

if __name__ == '__main__':
    api.add_resource(Company, "/company/<string:name>")
    app.run(debug=True)
	

######## NOTES: #########
#How to identify correct page:
#https://graph.facebook.com/v2.12/search?q=<COMPANYNAME>&type=<PAGE/EVENT/WHATEVER>&fields=<ABOUT, FAN_COUNT, WEBSITE>
#Get the one 	with max(fan_count) 
#				OR keyword OFFICIAL
#				OR .com.au in their website (since we're dealing with AU companies, hopefully)
