import re, time, errno
from urllib import request
from crawler import CrawlerHTMLParser
from crawler import SchedulerClient

class WebCrawler():
    # Regex for whole urls (http(s)://www.x.y/a/b)
    URL_REG = "^(https?://(?:www.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9].[^s]{2,}|www.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9].[^s]{2,}|https?://(?:www.|(?!www))[a-zA-Z0-9]+.[^s]{2,}|www.[a-zA-Z0-9]+.[^s]{2,})"
    
    # Regex for path urls (/a/b)
    URL_PATH_REG = "^(/[a-z0-9-._~%!$&'()*+,;=@]+(/[a-z0-9-._~%!$&'()*+,;=:@]+)*/?|/)"

    CONSECUTIVE_ERRORS_LIMIT = 10

    def __init__(self):
        self.parser = CrawlerHTMLParser.CrawlerHTMLParser()
        self.schedulerClient = SchedulerClient.SchedulerClient()

    def crawl(self):
        consecutive_errors = 0
        while True:
            try:
                url = self.schedulerClient.getUrl()

                # If scheduler server didn't return an url, then
                # try again after 1 second
                if not url:
                    time.sleep(1)
                    continue

                # Fetch html
                req = request.Request(url)
                res = request.urlopen(req)
                htmlBytes = res.read()
                html = htmlBytes.decode("utf8")

                # Parse html
                self.parser.clear()
                self.parser.feed(html)

                # Format urls and encode them into bytes
                urls = []
                for link in self.parser.links:
                    # 1. Check if the link is a whole url
                    if (re.search(self.URL_REG, link)):
                        urls.append(link.encode())
                    # 2. Check if the link is a path instead
                    elif (re.search(self.URL_PATH_REG, link)):
                        # Check if the target url is of form http(s)://www.x.y/
                        if (url[len(url) - 1] == "/"):
                            urls.append((url[0: len(url) - 1] + link).encode())
                        else:
                            urls.append((url + link).encode())

                # Send urls to the scheduler server
                self.schedulerClient.sendUrls(urls)
                consecutive_errors = 0

                # Sleep 1 second in order to not overload 
                # the target who is crawled
                time.sleep(1)

            except Exception as e:
                # Connection to the server failed
                if e.args and e.args[0] == errno.EPIPE:
                    self.schedulerClient.close_connection()
                    print("Connection to the server failed")
                consecutive_errors += 1
                if consecutive_errors > self.CONSECUTIVE_ERRORS_LIMIT:
                    print(f'Encountered {consecutive_errors} consecutive errors, aborting...')
                    exit(1)
                print("error: ", e)                
