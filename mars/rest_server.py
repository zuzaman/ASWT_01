from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, reqparse, fields, marshal

from mars.moon import Moon

app = Flask(__name__, statuc_url_path="")
api = Api(app)



def send_error_404():
    return make_response(jsonify({'Error': 'This page was not found!'}), 404)


def send_error_400():
    return make_response(jsonify({'Error': 'Incorrect request!'}), 400)


class MoonAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('drisemin', type=int, required=True,
                                   help='No Mars minutes provided', location='json')
        self.reqparse.add_argument('drisehours', type=int, required=True,
                                   help='No Mars hours provided', location='json')
        self.reqparse.add_argument('ddescendmin', type=int, required=True,
                                   help='No Mars minutes provided', location='json')
        self.reqparse.add_argument('ddescendhours', type=int, required=True,
                                   help='No Mars hours provided', location='json')
        self.reqparse.add_argument('prisemin', type=int, required=True,
                                   help='No Mars minutes provided', location='json')
        self.reqparse.add_argument('prisehours', type=int, required=True,
                                   help='No Mars hours provided', location='json')
        self.reqparse.add_argument('pdescendmin', type=int, required=True,
                                   help='No Mars minutes provided', location='json')
        self.reqparse.add_argument('pdescendhours', type=int, required=True,
                                   help='No Mars hours provided', location='json')

        super(MoonsAPI, self).__init__()

        def post(self):
            args = self.reqparse.parse_args()
            daimos = Moon()
            phobos = Moon()




@app.route('/mars/webservice/moons', methods=['POST'])
def process_request_to_calculate_overlap():
    if not request.json:
        return send_error_400()


# Create your views here.
def main(request):
    return render(request, 'mars/home.html')


def result(request):
    dInterval = request.POST['deimos_interval']
    pInterval = request.POST['phobos_interval']

    moon_ = Moon.objects.create(dInterval=request.POST['deimos_interval'], pInterval=request.POST['phobos_interval'])
    moon_.process_periods()
    moon_.generalise_time()
    overlap = moon_.calculate_overlap()
    moon_.save()

    return render(request, 'mars/result.html', {'overlap': overlap})


api.add_resource(MoonsAPI), '/mars/webservice/moons', endpoint='moon')


if __name__ == '__main__':
    app.-run(debug=True)
