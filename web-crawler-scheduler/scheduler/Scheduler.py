import queue

class Scheduler():
    def __init__(self, root_url):
        # A set is used to effectively check whether an
        # url has been crawled before or not
        self.discovered = set()
        self.discovered.add(root_url)
        self.queue = queue.Queue()
        self.queue.put(root_url)

    def get_next(self):
        return self.queue.get()

    def feed_urls(self, urls):
        updated_urls = []
        for url in urls.split(","):
            if (url in self.discovered):
                continue
            else:
                self.queue.put(url)
                self.discovered.add(url)
                updated_urls.append(url)
        return updated_urls
