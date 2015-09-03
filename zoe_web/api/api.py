from flask import jsonify, request, send_file, abort, Blueprint
from zipfile import is_zipfile


@app.route("/api/<int:user_id>/cluster/<int:cluster_id>/terminate")
def api_terminate_cluster(user_id, cluster_id):
    db = CAaaState()
    ret = {}
    if not db.check_user_id(user_id):
        ret["status"] = "unauthorized"
        return jsonify(**ret)

    cluster_id = str(cluster_id)
    cluster_list = db.get_clusters(user_id)
    if cluster_id not in cluster_list:
        return abort(404)
    if cluster_list[cluster_id]["user_id"] != user_id:
        ret["status"] = "unauthorized"
        return jsonify(**ret)

    if sm.terminate_cluster(cluster_id):
        ret["status"] = "ok"
    else:
        ret["status"] = "error"
    return jsonify(**ret)


@app.route("/api/<int:user_id>/container/<int:container_id>/logs")
def api_container_logs(user_id, container_id):
    db = CAaaState()
    ret = {}
    if not db.check_user_id(user_id):
        ret["status"] = "unauthorized"
        return jsonify(**ret)

    logs = sm.get_log(container_id)
    if logs is None:
        ret["status"] = "no such container"
        ret["logs"] = ''
    else:
        logs = logs.decode("ascii").split("\n")
        ret["status"] = "ok"
        ret["logs"] = logs
    return jsonify(**ret)


@app.route("/api/<int:user_id>/history/<app_id>/logs")
def api_history_log_archive(user_id, app_id):
    state = CAaaState()
    if not state.check_user_id(user_id):
        return jsonify(status="unauthorized")

    ah = AppHistory(user_id)
    path = ah.get_log_archive_path(app_id)
    return send_file(path, mimetype="application/zip")
