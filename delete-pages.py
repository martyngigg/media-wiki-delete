import bs4
import mwclient
import urllib2


def delete_unused_files(site):
    html = __get_html('/Special:UnusedFiles')
    for anchor in html.findAll('a', {'class': 'image'}):
        # Remove preceding forward slash from href.
        __delete_page(site.Pages[anchor['href'][1:]])


def delete_pages_in_category(site):
    html = __get_html('/Category:Algorithms')
    anchors = html.find('div', {'id': 'mw-pages'}).find_all('a')[1:-1]

    for anchor in anchors:
        __delete_page(site.Pages[anchor['href'][1:]])


def __get_html(segment):
    """
    Reads and stores the HTML of a given media-wiki page.

    Args:
        url (str): The url to append to the Mantid base URL.

    Returns:
        The HTML of the given webpage.
    """
    url = "http://" + MEDIA_WIKI_URL + segment
    return bs4.BeautifulSoup(urllib2.urlopen(url).read())


def __delete_page(page):
    """
    Attempts  to delete a given page from the media-wiki.

    Args:
        page (mwclient.page): The page to delete from the media-wiki.
    """
    if page.can('delete'):
        try:
            page.delete()
            print "Deleted the following page: " + page.name
        except:
            print "Error occured trying to delete " + page.name
    else:
        print 'Insufficent permission to delete page: ' + page.name


if __name__ == "__main__":
    MEDIA_WIKI_URL = 'www.mantidproject.org'

    site = mwclient.Site(MEDIA_WIKI_URL, path='/')
    site.login("username", "password")  # Assumes these are corect.

    # delete_unused_files(site)
    # delete_pages_in_category(site)
