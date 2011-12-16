from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError

from max.MADMax import MADMaxDB
from max.models import Activity
from max.exceptions import MissingField

from max.rest.ResourceHandlers import JSONResourceRoot, JSONResourceEntity


@view_config(route_name='activities', request_method='GET')
def UserActivities(context, request):
    """
         /users/{displayName}/activities

         Retorna all activities generated by a user
    """
    displayName = request.matchdict['user_displayName']

    mmdb = MADMaxDB(context.db)

    actor = mmdb.users.getItemsBydisplayName(displayName)[0]

    query = {'actor._id': actor['_id']}
    activities = mmdb.activity.search(query, sort="_id", flatten=1)

    handler = JSONResourceRoot(activities)
    return handler.buildResponse()


@view_config(route_name='activity', request_method='GET')
def UserActivity(context, request):
    """
         /users/{displayName}/activities/{activity}

         Mostra una activitat
    """

    #XXX Aqui potser no cal buscar l'usuari mes que per temes de comprovacions de seguretat
    displayName = request.matchdict['user_displayName']

    mmdb = MADMaxDB(context.db)
    actor = mmdb.users.getItemsBydisplayName(displayName)[0]
    activity_oid = request.matchdict['activity_oid']
    activity = mmdb.activity[activity_oid].flatten()

    handler = JSONResourceEntity(activity)
    return handler.buildResponse()


@view_config(route_name='activities', request_method='POST')
def AddUserActivity(context, request):
    """
         /users/{displayName}/activities

         Afegeix una activitat
    """
    displayName = request.matchdict['user_displayName']

    mmdb = MADMaxDB(context.db)
    actor = mmdb.users.getItemsBydisplayName(displayName)[0]
    rest_params = {'actor': actor}

    # Try to initialize a Activity object from the request
    # And catch the possible exceptions
    try:
        newactivity = Activity(request, rest_params=rest_params)
    except MissingField:
        return HTTPBadRequest()
    except ValueError:
        return HTTPBadRequest()
    except:
        return HTTPInternalServerError()

    # If we have the _id setted, then the object already existed in the DB,
    # otherwise, proceed to insert it into the DB
    # In both cases, respond with the JSON of the object and the appropiate
    # HTTP Status Code

    if newactivity.get('_id'):
        # Already Exists
        code = 200
    else:
        # New User
        code = 201
        activity_oid = newactivity.insert()
        newactivity['_id'] = activity_oid

    handler = JSONResourceEntity(newactivity.flatten(), status_code=code)
    return handler.buildResponse()
