import requests
import lxml.html as html

def get_article_links():
    max_security_page = 988
    base_url = "http://thinkprogress.org/security/issue/page/"
    all_urls = [base_url + str(i) + "/" for i in xrange(max_security_page)]
    all_articles = (get_articles_on_page(url) for url in all_urls)
    return all_articles
    
def get_articles_on_page(url):
    document = html.document_fromstring(requests.get(url).content)
    links = document.cssselect("h4 a")
    return [link.attrib["href"] for link in links]

def get_article_text(article_url):
    document = html.document_fromstring(requests.get(article_url).content)
    body = document.cssselect("div.post > *")
    links = document.cssselect("div.post")
    text_body = " ".join(filter(None, (thing.text for thing in body)))
    link_body = " ".join(filter(None, (thing.text for thing in links)))
    all_text = " ".join(filter(None, [text_body, link_body]))
    return all_text

def output_everything():
    output_file = "allData.txt"
    counter = 0
    with open(output_file, 'wb') as sink:
        for thing in get_article_links():
            for article in thing:
                counter += 1
                print counter
                sink.write(get_article_text(article).encode('utf8', 'ignore'))

output_everything()
