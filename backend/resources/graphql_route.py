from flask import Blueprint, request, jsonify, current_app
from ariadne import graphql_sync
from ariadne.explorer import ExplorerGraphiQL
from gql.index import schema

blp = Blueprint("graphql", __name__)

explorer_html = ExplorerGraphiQL().html(None)


@blp.route("/graphql", methods=["GET"])
def graphql_playground():
    return explorer_html, 200


@blp.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema, data, context_value=request, debug=current_app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code
