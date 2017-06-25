from flask_restplus import reqparse

recordings_arguments = reqparse.RequestParser()
recordings_arguments.add_argument('title', location='args', required=False, help='Title of the song')
recordings_arguments.add_argument('artist', location='args', required=False, help='Recording artist')
recordings_arguments.add_argument('album', location='args', required=False, help='Album')

works_arguments = reqparse.RequestParser()
works_arguments.add_argument('composer', location='args', required=False, help='Composer of the song')
works_arguments.add_argument('title', location='args', required=False, help='Title of the song')
