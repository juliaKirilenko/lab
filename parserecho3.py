from urllib.parse import urljoin
import urllib3
from datetime import datetime
from datetime import timedelta
from lxml import html
from csv import DictWriter
from urllib3.exceptions import ReadTimeoutError, NewConnectionError, MaxRetryError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ParserEcho:
    def __init__(self, filename):
        self.urls_xpath =  ".//h3//a/@href"
        self.name_xpath = "//meta[@property='og:title']/@content"
        self.desc_xpath = "//meta[@property='og:description']/@content"
        self.filename = filename
        self.root = 'https://echo.msk.ru/news/'
        self.http = urllib3.PoolManager(num_pools=30)
        
    def get_xpath(self, xpath,doc):
        item = doc.xpath(xpath)
        if item:
            return ' '.join(item[-1].split()) 
        return None
    
    def get_item(self, page_content):
   
        document = html.fromstring(page_content)
        name = self.get_xpath(self.name_xpath,document)
        desc = self.get_xpath(self.desc_xpath,document)

        return {'title': name, 'descr': desc}
    
    def get_news_from_page(self, page_con):
        count =0
        doc = html.fromstring(page_con)
        fieldnames = ['title', 'descr']
        for url in doc.xpath(self.urls_xpath):
            url = urljoin(self.root, url)
            t=self.get_conn(url)
            p = self.get_item(t)
            count=count+1
            with open(self.filename, 'a', encoding='utf-8') as f:
                writer = DictWriter(f, fieldnames = fieldnames)
                writer.writerow(p)
            
        print(count)
        
    def get_page_by_day(self, delta):
        now = datetime.now()-timedelta(delta) - timedelta(343) 
        url=urljoin(self.root,now.strftime("%Y/%m/%d"))
        r=self.get_conn(url)
        self.get_news_from_page(r)
    
    def get_conn(self, url):
        try:
            r = self.http.request('GET', url)
            if r.status == 200:
                return r.data
            else:
                print("Code", r.status, "at", url)
        except (NewConnectionError, MaxRetryError, ReadTimeoutError) as e:
            print(e.__class__.__name__, "at", url)