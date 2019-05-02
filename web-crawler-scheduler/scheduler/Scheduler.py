import queue

class Scheduler():
    def __init__(self, root_url):
        # A set is used to effectively check whether an
        # url has been crawled before or not
        self.discovered = set()
        self.discovered.add(root_url)

        # A queue is used to queue the found urls
        self.queue = queue.Queue()
        self.queue.put(root_url)

    def get_next(self):
        # Return the next url from the queue
        return self.queue.get()

    def feed_urls(self, urls):
        updated_urls = []
        for url in urls.split(","):
            # Don't add the url into the queue
            # if it has been discovered before
            if (url in self.discovered):
                continue
            else:
                # Add the url to the queue and the set
                self.queue.put(item=url)
                self.discovered.add(url)
                updated_urls.append(url)
        # Return the urls that were added into the queue
        return updated_urls
