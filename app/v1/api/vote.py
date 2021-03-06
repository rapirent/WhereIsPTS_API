import datetime

from flask import Blueprint, Response, current_app, jsonify, request

from app.models import Channel, Store, Vote, store_schema

vote_controller = Blueprint('vote_v1', __name__)


@vote_controller.route('/vote/store/<int:sid>', methods=['POST'])
def vote_store_channel(sid):

    store = Store.read(sid)
    if store:
        request_data = request.form
        cid = request_data.get('cid', None)

        if not cid:
            return Response(status=400)
        else:
            cid = int(cid)

        idx = -1
        for i, vote in enumerate(store.votes):
            if vote.cid == cid:
                idx = i
                break
        if idx >= 0:
            store.votes[idx].vote_count += 1
        else:
            channel = Channel.read(cid)
            vote = Vote(sid=sid, cid=cid, vote_count=1)
            if channel:
                store.votes.append(vote)
        success = store.update()
        if success:
            result = store_schema.dump(store)
            return jsonify(result.data), 200
        else:
            return Response(status=500)
    return Response(status=404)
