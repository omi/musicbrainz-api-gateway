import logging
import musicbrainzngs as mbz

from flask import request
from flask_restplus import Resource
from omi.api.gateway.parsers import recordings_arguments
from omi.api.restplus import api

log = logging.getLogger(__name__)
ns = api.namespace('recordings', description='Operations related to musical recordings')
mbz.set_useragent('omi', 1.0, 'omi@gmail.com')


@ns.route('/<matrix(limit=128, offset=0):params>')
class RecordingsCollection(Resource):
    """
    Manages a list of all recordings, and lets you POST to add new recording data
    """
    @api.expect(recordings_arguments)
    def get(self, params):
        """
        Returns list of recordings based on the query and URL parameters.
        """
        args = recordings_arguments.parse_args(request)
        offset = int(params['offset'])
        limit = int(params['limit'])
        title = args['title']
        artist = args['artist']
        album = args['album']
        results = mbz.search_recordings(query=title, limit=limit, offset=offset, strict=False, artist=artist, release=album)
        # print(results)
        return self.mbz_results_to_omi(offset, results)

    def mbz_results_to_omi(self, offset, results):
        converted = []
        for x in results['recording-list']:
            if type(x) is dict:
                converted.append({
                    'title': x['title'],
                    'artists': self.mbz_artists_to_omi(x['artist-credit']),
                    'releases': self.mbz_releases_to_omi(x['release-list']),
                    # 'raw': x,
                })
        return {
            'offset': offset,
            'count': len(converted),
            'total': results['recording-count'],
            'results': converted
        }

    def mbz_artists_to_omi(self, artists):
        converted = []
        for x in artists:
            if type(x) is dict:
                converted.append({
                    'name': x['artist']['name'],
                    'id': x['artist']['id'],
                })
        return converted

    def mbz_releases_to_omi(self, releases):
        converted = []
        for x in releases:
            if type(x) is dict:
                converted.append({
                    'date': x['date'] if 'date' in x else '',
                    'title': x['title'] if 'title' in x else '',
                })
        return converted
