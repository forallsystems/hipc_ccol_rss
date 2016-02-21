import jwt, time, datetime, requests, StringIO
from PyRSS2Gen import PyRSS2Gen
import settings, CustomRSSItem

def _generatePayLoad():
    return {"exp": int(time.time()),
           "version": "v1",
           'payload':{}}

#AWS Lambda Function
def feed_handler(event, context):    
    headers = {'Accept' : 'application/json',
               'Authorization' : 'JWT token =' + settings.CCOL_API_TOKEN}
    
    feedItems = []
    
    #Get the program metadata for each organization
    #http://chicago.col-engine-staging.com/apipie/1.0/programs/index.html
    for org_id in settings.ORG_LIST:
    
        program_api_url = "http://chicago.col-engine.com/partner_api/v1/orgs/"+str(org_id)+"/programs.json"
        
        payload = _generatePayLoad()
        jwt_string = jwt.encode(payload, settings.CCOL_API_SECRET)
        programs_request = requests.get(program_api_url+"?jwt="+jwt_string, data="", headers=headers)
        
        for program in programs_request.json()['result']:
            #For each program, get the scheduled_programs
            #http://chicago.col-engine-staging.com/apipie/1.0/scheduled_programs.html
            scheduled_program_api_url = "http://chicago.col-engine.com/partner_api/v1/orgs/"+str(org_id)+"/programs/"+str(program['id'])+"/scheduled_programs.json"
            
            payload = _generatePayLoad()
            jwt_string = jwt.encode(payload, settings.CCOL_API_SECRET)
            scheduled_programs_request = requests.get(scheduled_program_api_url+"?jwt="+jwt_string, data="", headers=headers)
        
            for scheduled_program in scheduled_programs_request.json()['result']:
                if not scheduled_program['hide']:
                    payment = "Free"
                    if scheduled_program['price'] == 1:
                        payment = "$1 to $50"
                    elif scheduled_program['price'] == 2:
                        payment = "$50+"
                        
                    categories = ""
                    for c in scheduled_program['categories']:
                        if c['category']['name']:
                            if categories:
                                categories+=", "
                            categories+=c['category']['name']

                    customItems = {"event_name":scheduled_program['name'],
                                   "event_description":scheduled_program['description'].encode("utf-8"),
                                   "event_start_date":scheduled_program['start_date'],
                                   "event_end_date":scheduled_program['end_date'],
                                   "event_start_time":scheduled_program['start_time'],
                                   "event_end_time":scheduled_program['end_time'],
                                   "event_organizer":scheduled_program['org_name'],
                                   "event_type":scheduled_program['meeting_type'],
                                   "event_website":scheduled_program['registration_url'],
                                   "event_image":scheduled_program['logo_url'],
                                   "event_cost":payment,
                                   "event_categories":categories,
                                   "venue_name":scheduled_program['location_name'],
                                   "venue_street_address":scheduled_program['address'],
                                   "venue_city":scheduled_program['city'],
                                   "venue_state":scheduled_program['state'],
                                   "venue_zipcode":scheduled_program['zipcode'],
                                   }
                        
                    feedItems.append(CustomRSSItem.CustomRSSItem(
                                         title = scheduled_program['name'],
                                         description = scheduled_program['description'].encode("utf-8"),
                                         link = scheduled_program['registration_url'],
                                         customItems = customItems
                                         ))
                  
    #Generate feed
    rss = PyRSS2Gen.RSS2(
        title = "Chicago City of Learning Events Feed",
        link = "",
        description = "The latest events from Chicago City of Learning organizations.",
        lastBuildDate = datetime.datetime.now(),
        items = feedItems)
    
    output = StringIO.StringIO()
    rss.write_xml(output)
    
    #Send back RSS/XML content
    return output.getvalue()