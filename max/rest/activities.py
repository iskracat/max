# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotImplemented, HTTPNoContent

from max.MADMax import MADMaxDB
from max.models import Activity
from max.decorators import MaxResponse, requirePersonActor
from max.oauth2 import oauth2
from max.exceptions import ObjectNotFound, Unauthorized, Forbidden

from max.rest.ResourceHandlers import JSONResourceRoot, JSONResourceEntity
from max.rest.utils import searchParams

import re

@view_config(route_name='user_activities', request_method='GET')
@MaxResponse
@oauth2(['widgetcli'])
@requirePersonActor
def getUserActivities(context, request):
    """
         Return all activities generated by a user.

         :rest username
    """
    mmdb = MADMaxDB(context.db)
    query = {}
    query['actor.username'] = request.actor['username']
    query['verb'] = 'post'
    chash = request.params.get('context', None)
    if chash:
        query['contexts.hash'] = chash

    is_head = request.method == 'HEAD'
    activities = mmdb.activity.search(query, sort="_id", keep_private_fields=False, squash=['favorites', 'likes'], flatten=1, count=is_head, **searchParams(request))

    handler = JSONResourceRoot(activities, stats=is_head)
    return handler.buildResponse()


@view_config(route_name='user_activities', request_method='POST')
@MaxResponse
@oauth2(['widgetcli'])
@requirePersonActor
def addUserActivity(context, request):
    """
        Adds a post to the user activities

        :rest username The username that will own the activity

        :query* {"object": {"objectType": "note", "content": ""}} The content of the activity
        :query {"contexts": {"objectType": "context", "url": ""}} The context of the activity
        :query {"generator": ""} The generator of the activity (i.e. "Twitter")
    """
    rest_params = {'actor': request.actor,
                   'verb': 'post'}

    # Initialize a Activity object from the request
    newactivity = Activity()
    newactivity.fromRequest(request, rest_params=rest_params)

    # New activity
    code = 201
    activity_oid = newactivity.insert()
    newactivity['_id'] = activity_oid

    handler = JSONResourceEntity(newactivity.flatten(squash=['keywords']), status_code=code)
    return handler.buildResponse()


@view_config(route_name='context_activities', request_method='GET')
@MaxResponse
@oauth2(['widgetcli'])
@requirePersonActor
def getActivities(context, request):
    """
         /context/{hash}/activities

         Return all activities, filtered by context.
    """
    chash = request.matchdict.get('hash', None)
    mmdb = MADMaxDB(context.db)

    # subscribed Uri contexts with read permission
    subscribed_uris = [ctxt['url'] for ctxt in request.actor.subscribedTo if 'read' in ctxt.get('permissions', []) and ctxt['objectType'] == 'context']

    # get the defined read context
    result_contexts = mmdb.contexts.getItemsByhash(chash)
    if result_contexts:
        rcontext = result_contexts[0]
    else:
        raise ObjectNotFound("Context with hash %s not found inside contexts" % (chash))
    url = rcontext['url']

    # regex query to find all contexts within url
    escaped = re.escape(url)
    url_regex = {'$regex': '^%s' % escaped}

    # search all contexts with public read permissions within url
    query = {'permissions.read': 'public', 'url': url_regex}
    public = [result.url for result in mmdb.contexts.search(query, show_fields=['url'])]

    query = {}                                                     # Search
    query.update({'verb': 'post'})                                 # 'post' activities
    query.update({'contexts.url': url_regex})                      # equal or child of url

    contexts_query = []
    if subscribed_uris:
        subscribed_query = {'contexts.url': {'$in': subscribed_uris}}  # that are subscribed contexts
        contexts_query.append(subscribed_query)                    # with read permission

    if public:                                                     # OR
        public_query = {'contexts.url': {'$in': public}}
        contexts_query.append(public_query)                        # pubic contexts

    is_head = request.method == 'HEAD'

    if contexts_query:
        query.update({'$or': contexts_query})

        sortBy_fields = {
            'activities': '_id',
            'comments': 'lastComment',
            'likes': 'likesCount'
        }
        sort_type = request.params.get('sortBy', 'activities')
        sort_order = sortBy_fields[sort_type]

        search_params = searchParams(request)
        # If we're in a 2+ page of likes
        if sort_type == 'likes' and 'before' in search_params and 'limit' in search_params:
            # Get the likes Count of the last object of the previous page
            last_page_object = mmdb.activity.search({'_id': search_params['before']})
            likes_count = last_page_object[0].likesCount
            # Target query to search items including the ones with the same likesCount than the last object
            # Widen the limit of resuts to the double as we may get duplicated results that we'll have to filter out later
            # the item referenced in before param will be included in the results of this search
            search_params['offset'] = likes_count + 1
            original_limit = int(search_params['limit'])
            search_params['limit'] = search_params['limit'] * 2

        activities = mmdb.activity.search(query, count=is_head, sort=sort_order, flatten=1, keep_private_fields=False, **searchParams(request))

        # If we're in a 2+ page of likes, continue filtering
        if sort_type == 'likes' and 'before' in search_params and 'limit' in search_params:
            start = 0
            for pos, activity in enumerate(activities):
                if activity['id'] == str(search_params['before']):
                    # We found the object referenced in before param, so we pick the next item as the first
                    start = pos + 1
                    break
            # Pick activities according to the original limit, excluding the ones included in the latest page
            activities = activities[start:start + original_limit]

    else:
        # we have no public contexts and we are not subscribed to any context, so we
        # won't get anything
        raise Forbidden("You don't have permission to see anyting in this context and it's child")

    handler = JSONResourceRoot(activities, stats=is_head)
    return handler.buildResponse()


@view_config(route_name='activity', request_method='GET')
@MaxResponse
@oauth2(['widgetcli'])
@requirePersonActor
def getActivity(context, request):
    """
         /activities/{activity}

         Returns an activity.
    """

    mmdb = MADMaxDB(context.db)
    activity_oid = request.matchdict['activity']
    activity = mmdb.activity[activity_oid].flatten()

    handler = JSONResourceEntity(activity)
    return handler.buildResponse()


@view_config(route_name='activity', request_method='DELETE')
@MaxResponse
@oauth2(['widgetcli'])
@requirePersonActor
def deleteActivity(context, request):
    """
    """
    mmdb = MADMaxDB(context.db)
    activityid = request.matchdict.get('activity', None)
    try:
        found_activity = mmdb.activity[activityid]
    except:
        raise ObjectNotFound("There's no activity with id: %s" % activityid)

    # Check if the user can delete the activity
    if found_activity.deletable:
        found_activity.delete()
    else:
        raise Unauthorized("You're not the owner of this activity, so you can't delete it")

    return HTTPNoContent()


@view_config(route_name='activity', request_method='PUT')
def modifyActivity(context, request):
    """
    """
    return HTTPNotImplemented()  # pragma: no cover
