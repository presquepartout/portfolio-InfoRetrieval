import requests
import urllib
import sys

DEBUG = False

def search_wikipedia(probe_string):
    """
    Given a string to search for, use the MediaWiki API to search Wikipedia.

    This is a generator function that will return all the page titles (which are typically "Q" strings).
    """
    query = {'action': 'query',
             'list': 'search',
             'srwhat': 'text',  # full text search
             'format': 'json',
             'srsearch': probe_string,
             'srnamespace': 0,
             'srinfo': 'totalhits',
             'srlimit': 'max',
             'continue': '',  # silence the warning about continuation data
             }
    totalhits = None
    returned_hits = 0
    seen = set()
    while True:
        # See: https://www.mediawiki.org/wiki/API:Search
        if DEBUG: print >> sys.stderr, 'Info: Making request from offset', query.get('sroffest', 0)
        r = requests.get('https://www.wikipedia.org/w/api.php', params=query)
        if DEBUG: print >> sys.stderr, r.url
        if r.status_code != 200:
            raise Exception("HTTPS request failed")

        # Get the results as a python dict (JSON -> python dict)
        json = r.json()

        # Show error or warnings
        if 'error' in json:
            print >> sys.stderr, 'Error:', json['error']
        if 'warnings' in json:
            print >> sys.stderr, 'Warning:', json['warnings']

        # Get the total hits if we haven't yet
        if totalhits is None:
            totalhits = json['query']['searchinfo']['totalhits']

        # Return the results (yield them to the caller)
        results = json['query']['search']
        for result in results:  # result is a dict
            title = result['title'].encode('utf8')
            url = 'https://www.wikipedia.org/wiki/%s' % urllib.quote(title.replace(' ', '_'))
            if url in seen:
                print >> sys.stderr, 'Warning: Duplicate URL returned: %s' % url
            seen.add(url)
            yield url

        # Break when we've returned all the expected hits, -OR- when return result is empty.
        # The latter is what you see if you set sroffset past the end.
        returned_hits += len(results)
        if returned_hits >= totalhits or len(results) == 0:
            break

        # Update continuation parameters to advance to the next window
        query['sroffset'] = json['continue']['sroffset']


if __name__ == '__main__':
	
    count = 4000
    n = 1
    name =
    for url in search_wikipedia("Thelonius Monk"):
    	with open("thelonius_monk_urls.txt", "ab") as f:    
        	f.write(url + "\n")
        if n == count:
            break
        n += 1
