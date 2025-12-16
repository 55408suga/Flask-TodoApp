from ariadne import make_executable_schema, load_schema_from_path
from gql.resolvers import query, todo

# .graphqlファイルを読み込む
type_defs = load_schema_from_path("gql/schema.graphql")

# スキーマとリゾルバ(query)を結合して、実行可能な状態にする
schema = make_executable_schema(type_defs, [query, todo])
