#!/usr/bin/env python3

from flask import jsonify
from flask import redirect
from urlhelper import UrlHelper


def action(request, req_obj):
    uh = UrlHelper()
    do_redirect = True
    if 'url' in req_obj:
        long_url = uh.longUrl(req_obj['url'])
        do_redirect = False
    else:
        long_url = uh.longUrl(request.url)

    if long_url:
        if do_redirect:
            return redirect(long_url, code=302)
        return jsonify({'status': 'SUCCESS', 'result': "{0}".format(long_url)}), 200, {}
    raise Exception('Invalid Response')


def main(request):
    try:
        req_obj = {}
        if request.method == 'POST':
            req_obj = request.get_json(silent=True)
        return action(request, req_obj)
    except Exception as e:
        return jsonify({'status': 'ERROR', 'result': str(e)}), 400, {}
