import requests
import random
import time
import json

# the user agent sent along with the http requests
header = {'User-Agent': 'vjean.homepage.img-fetcher'}


class RedditNugget(object):
    """A data unit for a reddit image post, storing its title, image,
    subreddit name, and permalink"""

    def __init__(self, title, img, post, sub):
        super(RedditNugget, self).__init__()
        self.title = title
        self.img = img
        self.post = post
        self.sub = sub


def purify(childList):
    result = []
    for c in childList:
        data = c['data']
        title = data['title']
        post = 'https://www.reddit.com' + data['permalink']
        sub = data['subreddit']

        # if the preview field doesn't exist,
        # there's no way to check the dimensions
        # or retrieve the image url
        try:
            src = data['preview']['images'][0]['source']
            if (src['width'] < src['height'] or src['width'] < 1500):
                continue
            img = data['preview']['images'][0]['source']['url']
            nugget = RedditNugget(title, img, post, sub)
            result.append(nugget)
        except KeyError:
            continue

    return result


def request_json(url):
    r = requests.get(url, headers=header)
    return r.json()


def get_random_redditnugget():
    f = open('bg_urls.json')
    l = json.load(f)

    n = l[random.randint(0, len(l) - 1)]

    f.close()
    return n


def fetch(verbose=False):
    start = time.clock()

    # max nb of images to fetch
    limit_img = 1000

    subreddits = ['earthporn', 'spaceporn', 'villageporn']
    posts = []

    url = "https://www.reddit.com/r/" \
        + '+'.join(subreddits) \
        + "/top.json?sort=top&t=all&count=25&after="

    if verbose:
        print("Pages visited :")

    # 25 images per reddit page
    while len(posts) < limit_img - 25:
        if verbose:
            print(url)
        # get json data
        page = request_json(url)
        # get img data
        posts = posts + purify(page['data']['children'])
        # update url
        x = url.find("&after=")
        after = page['data']['after']
        if verbose and after is None:
            print("no more pages.")
            break
        url = url[:x] + "&after=" + after

    end = time.clock()
    print("Fetched " + str(len(posts)) + " posts in " + str(round(end - start, 3)) + " seconds.")

    out_file = open('bg_urls.json', mode='w')
    json.dump([o.__dict__ for o in posts], out_file, indent=2)
    out_file.close()


if __name__ == "__main__":
    fetch(verbose=True)
