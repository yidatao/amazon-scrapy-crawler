## Readme

This is a simple web crawler built on [Scrapy](http://doc.scrapy.org/en/latest/index.html). It crawls  items on Amazon (e.g., [TVs](http://www.amazon.com/gp/search/ref=sr_nr_n_1?fst=as%3Aoff&rh=n%3A172282%2Cn%3A1266092011%2Cn%3A172659%2Ck%3ATV&keywords=TV&ie=UTF8&qid=1449805375&rnid=493964)), specifically each item's name, rating, reviews, and price.

#### Usage

Run the following command in the project's top-level directory
```
scrapy crawl amazon
```


#### Notes

 * Each crawled item goes through two pipelines. The first pipeline drops item with missing information.
 * The second pipeline inserts the item into database. Here I used [Twisted adbapi](http://www.leehodgkinson.com/blog/scrapy-pipelines/) for non-blocking DB access. 


#### Disclaimer

I created this crawler simply for learning Scrapy. If you want to use or extend this crawler, please first refer to Amazon's policy on data crawling and data usage.
