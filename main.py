from crawl import LinkCrawler, DataCrawler, ImageCrwaler

if __name__ == "__main__":
    crawler = LinkCrawler(cities=['paris', 'amsterdam', 'berlin'])
    crawler.start(store=True)

    data_crawler = DataCrawler()
    data_crawler.start(store=True)

    imaagecrawler = ImageCrwaler()
    imaagecrawler.start(store=True)
    

