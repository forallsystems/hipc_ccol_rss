from PyRSS2Gen import PyRSS2Gen

class CustomRSSItem(PyRSS2Gen.RSSItem):
    def __init__(self,
                 title = None,  # string
                 link = None,   # url as string
                 description = None, # string
                 author = None,      # email address as string
                 categories = None,  # list of string or Category
                 comments = None,  # url as string
                 enclosure = None, # an Enclosure
                 guid = None,    # a unique string
                 pubDate = None, # a datetime
                 source = None,  # a Source
                 
                 #custom hipc rss fields
                 start_date=None,
                 end_date=None,
                 start_time=None,
                 end_time=None,
                 venue=None,
                 venue_address=None,
                 venue_city=None,
                 venue_state=None,
                 event_type=None,
                 event_website=None,
                 event_image=None,
                 payment=None
                 ):
        
        PyRSS2Gen.RSSItem.__init__(self, title,link,description,author,categories,comments,enclosure,guid,pubDate,source)
      
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.venue = venue
        self.venue_address = venue_address
        self.venue_city = venue_city
        self.venue_state = venue_state
        self.event_type = event_type
        self.event_website = event_website
        self.event_image = event_image
        self.payment = payment
        
        
    def publish_extensions(self, handler):
        PyRSS2Gen._opt_element(handler, "start_date", self.start_date)
        PyRSS2Gen._opt_element(handler, "end_date", self.end_date)
        PyRSS2Gen._opt_element(handler, "start_time", self.start_time)
        PyRSS2Gen._opt_element(handler, "end_time", self.end_time)
        PyRSS2Gen._opt_element(handler, "venue", self.venue)
        PyRSS2Gen._opt_element(handler, "venue_address", self.venue_address)
        PyRSS2Gen._opt_element(handler, "venue_city", self.venue_city)
        PyRSS2Gen._opt_element(handler, "venue_state", self.venue_state)
        PyRSS2Gen._opt_element(handler, "event_type", self.event_type)
        PyRSS2Gen._opt_element(handler, "event_website", self.event_website)
        PyRSS2Gen._opt_element(handler, "event_image", self.event_image)
        PyRSS2Gen._opt_element(handler, "payment", self.payment)