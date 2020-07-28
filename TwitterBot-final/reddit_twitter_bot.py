import praw
import wget
import time
import os
import glob
import keys


def findMeme():
    reddit = praw.Reddit(client_id=reddit_keys["C_id"],
                         client_secret=reddit_keys["C_secret"],
                         user_agent=reddit_keys["User_agent"],
                         username=reddit_keys["Uname"],
                         password=reddit_keys["Password"])

    # print(reddit.read_only)  # Output: False
    extension = ""
    title=""
    permaLink=""
    subreddit = reddit.subreddit("MotivationalPics")

    #
    # print("name ",subreddit.display_name)  # Output: redditdev
    # print("tit ",subreddit.title)         # Output: reddit Development
    # print("desc ",subreddit.description)

    def checkImage(url):
        keys = ['jpg', 'png', 'webm', ]
        for key in keys:
            if url.find(key) != -1:
                print("true url", url)
                return True
        return False

    donePIds = []

    with open('donePostIDs.txt', 'r') as f:
        for line in f:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]

            # add item to the list
            donePIds.append(currentPlace)

    for submission in subreddit.hot():
        # print("tit ", submission.title)
        title = submission.title
        # permaLink = submission.permalink
        permaLink = submission.id # no need of the long link, we can directly get a shorter link by the id...using https://redd.it/id
        url = submission.url
        # print("url ", url)
        # print(type(submission.url))
        if submission.id not in donePIds:
            donePIds.append(submission.id)
            if checkImage(url):
                # wget.download(url,'img\\'+submission.title+url[-4:])
                files = glob.glob('img/*')
                for f in files:
                    print("F = ", f)
                    os.remove(f)
                wget.download(url, 'img\\output' + url[-4:])
                extension = url[-4:]

                # wget.download(url, 'img')
                print("downed")
                break
        # print("18 ", submission.over_18)
        # print("selfText ", submission.selftext)
        print("BREAK")

    with open('donePostIDs.txt', 'w') as f:
        for listitem in donePIds:
            f.write('%s\n' % listitem)

    return title, permaLink, extension


if __name__ == "__main__":
    _ = findMeme()
