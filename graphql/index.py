from ariadne import make_executable_schema, load_schema_from_path
from graphql.resolvers import query

# .graphqlファイルを読み込む
type_defs = load_schema_from_path("graphql/schema.graphql")

# スキーマとリゾルバ(query)を結合して、実行可能な状態にする
schema = make_executable_schema(type_defs, query)
