#!/usr/bin/env python3

from flask import jsonify
# from cloudlib import CloudFuncHelper
from urlhelper import UrlHelper


def action(request, req_obj):
    if req_obj:
        expires = None
        if 'expires' in req_obj:
            expires = req_obj['expires']

        uh = UrlHelper()
        short_url = uh.shortenUrl(req_obj['url'], expires)
        if short_url:
            return jsonify({'status': 'SUCCESS', 'result': "{0}".format(short_url)}), 200, {}

        raise Exception('Invalid Response')
    else:
        raise Exception("Invalid Request")


def main(request):
    try:
        req_obj = request.get_json(silent=True)
    except Exception as e:
        return jsonify({'status': 'ERROR', 'result': str(e)}), 400, {}

    return action(request, req_obj)
