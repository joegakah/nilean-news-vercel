from eventregistry import *
er = EventRegistry(apiKey = "df834c86-1e88-40c2-a363-78f0da04ef99")

# get the USA URI
usUri = er.getLocationUri("USA")    # = http://en.wikipedia.org/wiki/United_States

q = QueryArticlesIter(
    keywords = QueryItems.OR(["Hillary Clinton", "Sandra Bullock"]), 
    minSentiment = 0.4,
    sourceLocationUri = usUri,
    dataType = ["news", "blog"])

# obtain at most 500 newest articles or blog posts, remove maxItems to get all
for art in q.execQuery(er, sortBy = "date", maxItems = 500):
    print(art)