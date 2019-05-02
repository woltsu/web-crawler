import queue

class Scheduler():
    def __init__(self, root_url):
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
                self.queue.put(item=url)
                self.discovered.add(url)
                updated_urls.append(url)
        return updated_urls
