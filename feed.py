import jwt, time, datetime, requests, StringIO
from PyRSS2Gen import PyRSS2Gen
import settings, CustomRSSItem

def _generatePayLoad():
    return {"exp": int(time.time()),#+ 5 minutes TODO
           "version": "v1",
           'payload':{}}

#AWS Lambda Function
def feed_handler(event, context):    
    headers = {'Accept' : 'application/json',
               'Authorization' : 'JWT token =' + settings.CCOL_API_TOKEN}
    
    feed_items = []
    
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
                        
                    feed_items.append(CustomRSSItem.CustomRSSItem(
                                         title = scheduled_program['name'],
                                         description = scheduled_program['description'].encode("utf-8"),
                                         #Custom RSS Fields
                                         start_date=scheduled_program['start_date'],
                                         end_date=scheduled_program['end_date'],
                                         start_time=scheduled_program['start_time'],
                                         end_time=scheduled_program['end_time'],
                                         venue=scheduled_program['location_name'],
                                         venue_address=scheduled_program['address'],
                                         venue_city=scheduled_program['city'],
                                         venue_state=scheduled_program['state'],
                                         event_type=scheduled_program['meeting_type'],
                                         event_website=scheduled_program['registration_url'],
                                         event_image=scheduled_program['logo_url'],
                                         payment=payment
                                         ))
                  
    #Generate feed
    rss = PyRSS2Gen.RSS2(
        title = "CCOL Events Feed",
        link = "",
        description = "The latest events from Chicago City of Learning organizations.",
        lastBuildDate = datetime.datetime.now(),
        items = feed_items)
    
    output = StringIO.StringIO()
    rss.write_xml(output)
    
    #Send back RSS/XML content
    return output.getvalue()

