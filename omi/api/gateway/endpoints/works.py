import logging
import musicbrainzngs as mbz

from flask import request
from flask_restplus import Resource
from omi.api.gateway.parsers import works_arguments
from omi.api.restplus import api

log = logging.getLogger(__name__)
ns = api.namespace('works', description='Operations related to musical works')
mbz.set_useragent('omi', 1.0, 'omi@gmail.com')

@ns.route('/<matrix(limit=128, offset=0):params>')
class WorksCollection(Resource):
    """
    Manages a list of all recordings, and lets you POST to add new recording data
    """
    @api.expect(works_arguments)
    def get(self, params):
        """
        Returns list of works based on the query and URL parameters.
        """
        args = works_arguments.parse_args(request)
        offset = int(params['offset'])
        limit = int(params['limit'])
        composer = args['composer']
        title = args['title']
        results = mbz.search_works(query=title, limit=limit, offset=offset, strict=False,artist=composer)
        print(results)
        return self.mbz_results_to_omi(offset, results)

    def mbz_results_to_omi(self, offset, results):
        converted = []
        for x in results['work-list']:
            if type(x) is dict:
                converted.append({
                    'title': x['title'],
                    'composers': self.mbz_artist_relationships_to_omi(x['artist-relation-list'],'composer') if x.has_key('artist-relation-list') else [],
                    'songwriters': self.mbz_artist_relationships_to_omi(x['artist-relation-list'],'lyricist') if x.has_key('artist-relation-list') else [],
#                    'raw': x
                })
        return {
            'offset': offset,
            'count': len(converted),
            'total': results['work-count'],
            'results': converted
        }

    def mbz_artist_relationships_to_omi(self, artists, role):
        converted = []
        for x in artists:
            if type(x) is dict and x['type'] == role:
                converted.append({
                    'name': x['artist']['name'],
                    'role': x['type'],
                    'id': x['artist']['id']
                })
        return converted

