## オープンデータ検索API
https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_search

## 50件読み出し
curl -X GET "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_search?q=*:*&rows=50&start=0"


## 検索APIのパラメータ
- q (文字列)
solr クエリ。オプション。デフォルト： "*：*"

- fq (文字列)
適用するフィルター クエリ。注: +site_id:{ckan_site_id} は、クエリが実行される前にこの文字列に追加されます。

- sort (string) 
検索結果の並べ替え。オプション。デフォルト: 「関連性 asc、metadata_modified desc」。 solr のドキュメントによると、これはフィールド名と並べ替え順序をカンマで区切った文字列です。

- rows (int) 
返される一致する行の数。クエリごとに 1000 データセットというハード制限があります。

- start (int) 
返されたデータセットのセットが開始される完全な結果内のオフセット。

- facet (文字列) 
ファセット結果を有効にするかどうか。デフォルト: True。

- facet.mincount (int) 
ファセット フィールドの最小カウントが結果に含まれる必要があります。

- facet.limit (int) 
ファセット フィールドが返す値の最大数。負の値は無制限を意味します。これは、search.facets.limit 構成オプションを使用してインスタンス全体に設定できます。デフォルトは50です。

- facet.field (文字列のリスト) 
ファセット対象のフィールド。デフォルトは空です。空の場合、返されるファセット情報は空です。

- include_drafts (bool)
True の場合、ドラフト データセットが結果に含まれます。ユーザーには自分のドラフト データセットのみが返され、システム管理者にはすべてのドラフト データセットが返されます。オプションで、デフォルトは False です。

- include_private (bool) 
True の場合、プライベート データセットが結果に含まれます。ユーザーの組織からのプライベート データセットのみが返され、システム管理者にはすべてのプライベート データセットが返されます。オプションで、デフォルトは False です。

- use_default_schema (bool) 
IDatasetForm プラグインで定義されたカスタム スキーマの代わりにデフォルトのパッケージ スキーマを使用します (デフォルト: False)