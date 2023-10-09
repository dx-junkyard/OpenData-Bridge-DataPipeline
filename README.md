# OpenDataの自動取得と整形
GitHub Actionsで定期的にPythonを実行し、公開されているOpenDataを取得、整形、GitHub Pagesで公開をします。

https://mitsuo-koikawa.github.io/Actions_Debug/

GitHub Pagesは公開Repositoryになるため、OpenDataの取得やファイル保存に必要な各種トークンはRepositoryのSecretに保存します。
GitHubは容量制限がありますし、Actionsの処理は遅めなので大容量のデータ処理には向きません。

# 設定方法
```
README.md       : このファイル
fetch.py        : OpenDataを読み込むPython Script
opendata.yml    : 読み込むデータのリンク集
.github/
  workflows/
    main.yml    : Actions Workflow設定ファイル
docs/           : GitHub Pages公開ページ
  index.html    : Pythonで自動生成されるTop Page
  data/         : 取得されたOpenDataの保存場所
  images/       : 各種画像ファイル
```
[手順]
1. RepositoryのClone
1. ローカル環境でのPython動作確認
1. 新しいRepository作成
1. 取得したOpenDataを公開するPagesの設定
1. Actionsでスクリプトの自動実行設定


## RepositoryのClone
Cloneしたいフォルダを作成し、そのフォルダの中で以下を実行します。
> git clone https://github.com/Mitsuo-Koikawa/Actions_Debug.git .

## ローカル環境でのPython動作確認
opendata.yml ファイルを編集して、アクセスをしたいOpenDataの情報を登録して、以下を実行してください。

> python3 fetch.py  

docs/dataフォルダーの中に取得したデータが登録され、そのデータへのリンクを含んだindex.mdが自動作成されます。以前に取得したデータは残りません。

## 新しいRepository作成
新しいRepositoryをGitHubのWeb画面上で作成し、動作確認をしたローカルのRepositoryをPushしてください。詳細は他のサイトをご参照ください。

### Secretの設定
Workflowでは内部的にGITHUB_TOKENを取得していますが、Google DriveやTableau Publicなどに出力する際に必要なトークンはSecretに保存をしてWorkflowの中で読み出す事が出来ます。これは公開Repositoryでも他の人に読まれることはありません。

Repositoryの管理画面の一番下の方にある [Secrets and variables] を開いて、[Actions] を選んでください。
[New repository secret] というボタンを押して、使用するアクセストークンを以下の名前で登録してください。
> ACTIONS_TOKEN

作成したSecretはWorkflowのYAMLで `${{ secrets.ACTIONS_TOKEN }}` として読み出す事が出来ます。  

### Google Driveの設定
変換スクリプトが整形データをGoogle Driveに書き込むためのトークンは
環境変数 `GGLDRIVE_TOKEN` に設定されています。
Pythonでは `os.environment` で参照してください。

トークンを変更するためには、GitHub RepositoryのSettingの
中のSecretsで、ActionsのSecretsの `GGLDRIVE_TOKEN`
を編集してください。WorkflowのYAMLの中でSecretsが
仮想環境の環境変数にコピーされています。

## Pagesの設定
GitHub Pagesを表示するためのBranchを作成します。静的HTML出力において少しの設定ミスでRepositoryが上書きされてしまうので、出力用のBranchを用意する事が安全です。本Workflowでは以下のExtensionを使用してPagesの出力を行っています。  
https://github.com/peaceiris/actions-gh-pages

> 出力先Branch: gh-pages  
ソースフォルダ: ./docs  
Jeykll処理: 有効 (Markdown処理に使用)  


## Actionsの設定
Repositoryの`Actions`タブを選んで`New workflow`を選んでください。設定ファイルとして以下のファイルを登録してください。
> .github/workflows/main.yml

上記 YAMLファイルの中の数値を変更する事で実行する周期を指定できます。

ActionsはDefaultではほぼログを出さないため、Debugのためには
以下のページにある設定をしてログ出力をさせてください。  
https://docs.github.com/ja/actions/monitoring-and-troubleshooting-workflows/enabling-debug-logging

```
on:  
  schedule:  
    - cron: '60 * * * *' # Every hour  
```

Actionsは実行に時間がかかるので、あまり小さい数字にしないでください。

main.ymlのWorkflowが実行されると以下の処理が自動で発行されます。すべて完了するまでPagesは一時的に表示できなくなります。  
1. main.yml
    1. ubuntu/latest上でのPython環境構築
    1. Pythonによるデータの取得
    1. ExtensionによるGit Hub Pagesへの出力
1. GitHub自動処理
    1. Pagesの自動再構築
