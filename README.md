# web-crawler
A web crawler that seeks for urls. Currently it doesn't serve any purpose apart from collecting different urls it finds across the web.
## Getting Started

### Prerequisites

- Python >= 3
- pipenv

OR

- Docker Compose


### Installing

Navigate to the project root and run the following command:
```bash
ROOT_URL=X docker-compose up --build --scale web-crawler=1
```

OR

Create a .env file to _web-crawler-scheduler_ directory and add a variable `ROOT_URL` into the file. Then open two seperate terminals and navigate to both _web-crawler-scheduler_ and _web-crawler_ directories, where in both run first the following command:

```bash
pipenv install
```

and then

```bash
pipenv run python main.py
```

### Disclaimer
Please notice that this project was created just to practise network programming with Python. If you choose to test this app, be sure to not overload the servers you are targeting. Don't start too many crawlers at once and don't remove the `time.sleep(1)` that slows down the loop in `WebCrawler.py` file. I'm not liable for any misuse of this application.
