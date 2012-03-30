from celery.task import task
from maxrules.twitter import twitter_generator_name, debug_hashtag, max_server_url
import requests
import pymongo
from maxrules.config import mongodb_url, mongodb_db_name
from max.MADMax import MADMaxCollection
from max.rest.utils import canWriteInContexts
from max.rest.utils import findHashtags
import logging


@task
def processTweet(twitter_username, content):
    """ Process inbound tweet
    """
    conn = pymongo.Connection(mongodb_url)
    db = conn[mongodb_db_name]
    users = MADMaxCollection(db.users)
    contexts = MADMaxCollection(db.contexts)

    # Parse text and determine the second or nth hashtag
    possible_hastags = findHashtags(content)
    query = [dict(twitterHashtag=hashtag) for hashtag in possible_hastags]

    if debug_hashtag in possible_hastags:
        return "Debug hastagh detected! %s" % content

    # Check if twitter_username is a registered for a valid MAX username
    # if not, discard it
    maxuser = users.search({"twitterUsername": twitter_username})
    if maxuser:
        maxuser = maxuser[0]
    else:
        return "Discarding %s tweet: Not such MAX user" % twitter_username

    # Check if hashtag is registered for a valid MAX context
    # if not, discard it
    maxcontext = contexts.search({"$or": query})
    if maxcontext:
        for context in maxcontext:
            # Check if MAX username has permission to post to the MAX context
            # if not, discard it
            try:
                can_write = canWriteInContexts(maxuser, [context.url])
            except:
                can_write = False

            if not can_write:
                return "Discarding %s tweet: MAX user can't write to specified MAX context" % maxuser.username

            # Construct the payload with the activity information
            newactivity = {
                "object": {
                    "objectType": "note",
                    "content": content
                },
                "contexts": [
                    context.url,
                ],
                "generator": twitter_generator_name
            }

            # Use the restricted REST endpoint for create a new activity in the specified
            # MAX context in name of the specified MAX username

            re = requests.post('%s/admin/people/%s/activities' % (max_server_url, maxuser.username), newactivity, auth=('admin', 'admin'), verify=False)
            if re.status_code == 201:
                return "Successful tweet insertion from user %s in context %s" % (maxuser, maxcontext)
            else:
                return "Error accessing the MAX API at %s" % max_server_url
    else:
        return "Discarding %s tweet: Not such MAX context" % maxuser.username
