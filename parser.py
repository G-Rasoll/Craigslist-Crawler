from bs4 import BeautifulSoup


class AdvertisementParser:

    def __init__(self):
        self.soup = None

    @property
    def title(self):
        title = self.soup.find('span', attrs={'id': 'titletextonly'})
        if title:
            return title.text

    @property
    def price(self):

        price = self.soup.find('span', attrs={"class": "price"})
        if price:
            return price.text

    @property
    def body(self):

        body = self.soup.find('section', attrs={'id': 'postingbody'})
        if body:
            return body.text

    @property
    def post_id(self):
        selector = "body > section > section > section >" \
                   " div.postinginfos > p:nth-child(1)"
        post_id = self.soup.select_one(selector)

        # post_id = self.soup.select("p.postinginfo")

        if post_id:
            return post_id.text.replace("Id publi: ", "")

    @property
    def time_created(self):
        # create_time_post = self.soup.find('p',
        #                                attrs={'class': 'postinginfo reveal'})

        time_selector = "body > section > section > section >" \
                        " div.postinginfos > p:nth-child(2) > time"

        create_time_post = self.soup.select_one(time_selector)
        if create_time_post:
            return create_time_post.attrs["datetime"]

    @property
    def images(self):
        images_list = self.soup.find_all('img')
        images_sources = set(
            [img.attrs['src'].replace('50x50c', '600x450') for img in
             images_list])
        return [{"url": src, 'flag': False} for src in images_sources]

    def parser(self, html_doc):
        self.soup = BeautifulSoup(html_doc, 'html.parser')

        dict_data = dict(
            title=self.title, price=self.price, body=self.body,
            post_id=self.post_id, images=self.images,
            create_at=self.time_created
        )

        return dict_data
