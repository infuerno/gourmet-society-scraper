import base64
import scraperwiki
import requests
from lxml import etree

def crawl(latitude):
    base_url = "https://www.gourmetsociety.co.uk/ajax/markers.php?"
    url = base_url + "restaurant="
#   url += "&location=Edinburgh"
    url += "&lat=" + str(latitude)
    url += "&lng=-5"
    url += "&radius=100"
    url += "&friday=false"
    url += "&saturday=false"
    url += "&sunday=false"
    url += "&december=false"
    url += "&offer="
    url += "&cuisine="
    
    headers = {
      'Referer' : 'https://www.gourmetsociety.co.uk/search.php?country=uk'
    }
    xml = requests.get(url, headers=headers).content
    dom = etree.fromstring(xml)
    
    for marker in dom.xpath('/markers/marker'):
        restaurant = {
          'address' : base64.b64decode(marker.xpath('@address')[0]).decode('latin1'),
          'address2' : base64.b64decode(marker.xpath('@address2')[0]),
          'chain_logo' : base64.b64decode(marker.xpath('@chain_logo')[0]),
          'city' : base64.b64decode(marker.xpath('@city')[0]),
          'county' : base64.b64decode(marker.xpath('@county')[0]),
          'cuisine' : base64.b64decode(marker.xpath('@cuisine')[0]),
          'id' : base64.b64decode(marker.xpath('@id')[0]),
          'latitude' : base64.b64decode(marker.xpath('@lat')[0]),
          'longitude' : base64.b64decode(marker.xpath('@lng')[0]),
          'name' : base64.b64decode(marker.xpath('@name')[0]).decode('latin1'),
          'name4url' : base64.b64decode(marker.xpath('@name4url')[0]),
          'postcode' : base64.b64decode(marker.xpath('@postcode')[0]),
          'tel' : base64.b64decode(marker.xpath('@tel')[0]).decode('latin1'),
          'thumb0' : base64.b64decode(marker.xpath('@thumb0')[0]),
          'thumb1' : base64.b64decode(marker.xpath('@thumb1')[0]),
          'type' : base64.b64decode(marker.xpath('@type')[0]),
          'web' : base64.b64decode(marker.xpath('@web')[0])
        }
        # Saving data:
        scraperwiki.sqlite.save(unique_keys=['id'], data=restaurant)
        # scraperwiki.sql.save(unique_keys, restaurant)


#UK Bounding Box:
#NE 60.854691, 1.768960
#SW 49.162090, -13.413930

for latitude in range(50,60):
    print "Crawling for latitude " + str(latitude) 
    crawl(latitude)
