from flask import Blueprint, request, jsonify, render_template_string
from backend.graphql_schema import schema

graphql_bp = Blueprint("graphql_bp", __name__)

GRAPHIQL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>FalcoVita GraphQL PlayGround</title>
  <link href="https://cdn.jsdelivr.net/npm/graphiql@3.0.6/graphiql.min.css" rel="stylesheet" />
  <style>
    body {
      margin: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: 'Inter', sans-serif;
    }
    #graphiql {
      height: 100vh;
    }
  </style>
</head>
<body>
  <div id="graphiql">Loading GraphQL Playground...</div>
  <script crossorigin src="https://cdn.jsdelivr.net/npm/react@18.2.0/umd/react.production.min.js"></script>
  <script crossorigin src="https://cdn.jsdelivr.net/npm/react-dom@18.2.0/umd/react-dom.production.min.js"></script>
  <script crossorigin src="https://cdn.jsdelivr.net/npm/graphiql@3.0.6/graphiql.min.js"></script>
  <script>
    const fetcher = GraphiQL.createFetcher({ url: '/graphql' });
    ReactDOM.render(
      React.createElement(GraphiQL, { 
        fetcher: fetcher,
        defaultQuery: "# Welcome to FalcoVita GraphQL API\\n# Try writing a query like:\\n# {\\n#   doctors {\\n#     id\\n#     specialization\\n#     user {\\n#       name\\n#       email\\n#     }\\n#   }\\n# }\\n"
      }),
      document.getElementById('graphiql'),
    );
  </script>
</body>
</html>
"""

@graphql_bp.route("/graphql", methods=["GET", "POST"])
def graphql_handler():
    if request.method == "GET":
        # Check if the client wants HTML (GraphiQL interface)
        if "text/html" in request.headers.get("Accept", ""):
            return render_template_string(GRAPHIQL_TEMPLATE)
        return jsonify({"message": "Use POST method for queries or request text/html to load GraphiQL"}), 400

    # Handle POST request
    data = request.get_json() or {}
    query = data.get("query")
    variables = data.get("variables")
    operation_name = data.get("operationName")

    if not query:
        return jsonify({"errors": [{"message": "Must provide query string"}]}), 400

    result = schema.execute(
        query,
        variable_values=variables,
        operation_name=operation_name,
        context_value={"request": request}
    )

    response = {}
    if result.errors:
        response["errors"] = [error.formatted for error in result.errors]
    if result.data is not None:
        response["data"] = result.data

    # Return status 200 even on errors, as per GraphQL specification
    return jsonify(response), 200
