#
# IMPORT Routines
#

from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, reqparse, fields, marshal
from mars.moon import Moon
from flask_cors import CORS, cross_origin

#
# Define global instances, required for Flask and its REST API
#
app = Flask(__name__, static_url_path="")
CORS(app)
api = Api(app)


def check_input(args):
    if (args['drisehour'] is None) or (args['drisemin'] is None) or (args['ddescenthour'] is None) or (
            args['ddescentmin'] is None):

        return "Not all Deimos data correctly provided"

    elif (args['prisehour'] is None) or (args['prisemin'] is None) or (args['pdescenthour'] is None) or (
            args['pdescentmin'] is None):

        return "Not all Phobos data provided"

    elif ((args['drisehour'] > 24) or (args['drisehour'] < 0)) or (
            (args['ddescenthour'] > 24) or (args['ddescenthour'] < 0)) or (
            (args['prisehour'] > 24) or (args['prisehour'] < 0)) or (
            (args['pdescenthour'] > 24) or (args['pdescenthour'] < 0)):

        return "Mars hours may only have the values between 00 and 24"

#    elif args['drisehour'] args['ddescenthour' args['prisehour'] args['pdescenthour']

    elif ((args['drisemin'] > 99) or (args['drisemin'] < 0)) or (
            (args['ddescentmin'] > 99) or (args['ddescentmin'] < 0)) or (
            (args['prisemin'] > 99) or (args['prisemin'] < 0)) or (
            (args['pdescentmin'] > 99) or (args['pdescentmin'] < 0)):
        return "Mars minutes may only have the values between 00 and 99"

    else:
        return None

def calculate_overlap(deimos, phobos):
    """
    Function that takes two inputs of the moon class in order to calculate the overlap
    This is done by taking running through a set of if-causes to determine the correct scenario.

    :param deimos: Instance of moon class
    :param phobos: Instance of moon class
    :return: The overlap of Mars minutes in an integer
    """

    # Deimos rises before Phobos

    if deimos.riseTime < phobos.riseTime:
        # Exc. 1
        # Twilight Rule - when Deimos descends in the same minute Phobos ascends
        # Results in one minute of overlap

        if deimos.descentTime == phobos.riseTime:
            return 1
        # Case 1
        # Deimos descends before Phobos rises
        # Results in no overlap

        elif deimos.descentTime < phobos.riseTime:
            return 0

        # Case 2
        # Deimos descends after Phobos rose and before / same time when Phobos descended
        # Results in an overlap between the ascent of Phobos and descent of Deimos

        elif deimos.descentTime <= phobos.descentTime:
            return deimos.descentTime - phobos.riseTime

        # Case 3
        # Deimos descends after Phobos rose and after Phobos descended.
        # Overlap based on time between ascent and descent of Phobos

        elif phobos.descentTime < deimos.descentTime:
            return phobos.descentTime - phobos.riseTime

    # Phobos rises before Deimos
    if phobos.riseTime < deimos.riseTime:

        # Exc. 2
        # Twilight Rule - when Deimos ascends in the same minute Phobos descends
        # Results in one minute of overlap
        if phobos.descentTime == deimos.riseTime:
            return 1

        # Case 4
        # Phobos descends before Deimos rises
        # Results in no overlap
        elif phobos.descentTime < deimos.riseTime:
            return 0

        # Case 5
        # Phobos descends after Deimos ascends, but before or at the same time it descends
        # Results in an overlap between the ascent of Deimos and the descent of Phobos
        elif phobos.descentTime <= deimos.descentTime:
            return phobos.descentTime - deimos.riseTime

        # Case 6
        # Phobos descends after Deimos ascends and descends
        # Results in an overlap between the the ascent of Deimos and the descent of Deimos
        elif deimos.descentTime < phobos.descentTime:
            return deimos.descentTime - deimos.riseTime

    # If they rise at the same time
    if phobos.riseTime == deimos.riseTime:

        # Case 7
        # If Deimos descends before Phobos
        # Results in an overlap between the ascent of Deimos and the descent of Deimos
        if deimos.descentTime < phobos.descentTime:
            return deimos.descentTime - deimos.riseTime

        # Case 8
        # If Phobos descends before Deimos or at the same time
        # Results in an overlap between the ascent of Phobos and the descent of Phobos

        if phobos.riseTime <= deimos.riseTime:
            return phobos.descentTime - phobos.riseTime


class MoonAPI(Resource):
    def __init__(self):
        """
        Init method used to parse the received arguments from the browser client.
        4 arguments per moon are received: Time of ascent in hours and minutes
        and the time of descent in hours and minutes.

        For each argument, integer is sat as required type. In case not delivered,
        an error message is sent through the RequestParser with the provided comment.
        """
        #
        # Parse request and define arguments
        #
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('drisemin', type=int, required=True,
                                   help='No Deimos ascent minutes provided', location='json')

        self.reqparse.add_argument('drisehour', type=int, required=True,
                                   help='No Deimos ascent hours provided', location='json')
        self.reqparse.add_argument('ddescentmin', type=int, required=True,
                                   help='No Deimos descent minutes provided', location='json')
        self.reqparse.add_argument('ddescenthour', type=int, required=True,
                                   help='No Deimos descent hours provided', location='json')
        self.reqparse.add_argument('prisemin', type=int, required=True,
                                   help='No Phobos ascent minutes provided', location='json')
        self.reqparse.add_argument('prisehour', type=int, required=True,
                                   help='No Phobos ascent hours provided', location='json')
        self.reqparse.add_argument('pdescentmin', type=int, required=True,
                                   help='No Phobos descent minutes provided', location='json')
        self.reqparse.add_argument('pdescenthour', type=int, required=True,
                                   help='No Phobos descent hours provided', location='json')

        super(MoonAPI, self).__init__()

    def post(self):
        """
        The method called in case a POST request is received by the REST API

        :param self: USed to call the Resource methods
        :return: Integer value showing the overlap in minutes when both moons can be seen
        """
        args = self.reqparse.parse_args()
        error = check_input(args)
        if error is not None:
            return {'error': error}

        daimos = Moon(args['drisehour'], args['drisemin'], args['ddescenthour'], args['ddescentmin'])
        phobos = Moon(args['prisehour'], args['prisemin'], args['pdescenthour'], args['pdescentmin'])

        return {'overlap': calculate_overlap(daimos, phobos)}


#
# This function creates the URI information for the REST API
#
api.add_resource(MoonAPI, '/mars/webservice/moon', endpoint='moon')

if __name__ == '__main__':
    app.run(debug=True)
