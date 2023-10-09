GitHub Actionsから実行されるPythonで、GitHub ActionsのBuildで生成されたログをGoogle Driveに自動的にアップロードするための手順は以下の通りです：

1. **Google Drive APIのセットアップ**:
   - [Google Cloud Console](https://console.cloud.google.com/)にアクセスして、新しいプロジェクトを作成します。
   - Drive APIを有効にします。
   - OAuth 2.0 クライアントIDを作成し、`credentials.json`をダウンロードします。
   - この`credentials.json`を使用して、アクセストークンを取得します。このトークンは、GitHub Secretsに保存することができます。

2. **GitHub Repositoryのセットアップ**:
   - リポジトリのルートに`.github/workflows`ディレクトリを作成し、その中にYAMLファイル（例：`upload_logs.yml`）を作成します。
   - `credentials.json`とアクセストークンをGitHub Secretsに保存します。

3. **GitHub Actions Workflowの作成**:
   - `.github/workflows/upload_logs.yml`に以下の内容を追加します：

```yaml
name: Upload Logs to Google Drive

on: [push, pull_request]

jobs:
  upload_logs:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

    - name: Upload logs to Google Drive
      run: python .github/scripts/upload_logs.py
      env:
        CREDENTIALS: ${{ secrets.GDRIVE_CREDENTIALS }}
        TOKEN: ${{ secrets.GDRIVE_TOKEN }}
```

4. **Pythonスクリプトの作成**:
   - `.github/scripts/upload_logs.py`というPythonスクリプトを作成し、以下の内容を追加します：

```python
import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive(filename, credentials, token):
    creds = Credentials.from_authorized_user(token)
    service = build('drive', 'v3', credentials=creds)

    media = MediaFileUpload(filename, mimetype='text/plain')
    file_metadata = {'name': os.path.basename(filename)}
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded {filename} to Google Drive with ID {file.get('id')}")

if __name__ == "__main__":
    # GitHub Actionsのログファイルのパスを指定
    log_file_path = "path_to_your_log_file.log"

    credentials = os.environ.get("CREDENTIALS")
    token = os.environ.get("TOKEN")

    if not credentials or not token:
        print("Credentials or token not provided.")
        sys.exit(1)

    upload_to_drive(log_file_path, credentials, token)
```

5. **GitHub Actionsの実行**:
   - このセットアップを完了すると、GitHub Actionsがトリガーされるたびに、ログファイルがGoogle Driveにアップロードされます。

注意: この例は基本的なものであり、実際の使用には適切なエラーハンドリングやその他の最適化が必要です。


Google Driver APIをプロジェクトの中で有効にする。
https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project=884554169139

このエラーは、Google Cloud Platform (GCP) のサービスアカウントのJSONキーが正しくないか、不完全であることを示しています。具体的には、JSONキーの`type`フィールドが`"service_account"`でなければならないのに、空または異なる値になっていることを示しています。

以下の手順でこのエラーを解消できる可能性があります：

1. **新しいサービスアカウントキーを生成**:
   - GCPコンソールにログインします。
   - 左側のナビゲーションメニューから「IAM & 管理」>「サービスアカウント」を選択します。
   - 問題のあるサービスアカウントを見つけ、右側の「キー」タブをクリックします。
   - 「キーの追加」>「JSON」を選択して新しいキーを生成します。
   - 生成されたキーをダウンロードし、GitHub Actionsの秘密として保存または使用します。

2. **キーの内容を確認**:
   - ダウンロードしたJSONキーをテキストエディタで開き、`type`フィールドが`"service_account"`となっていることを確認します。

3. **GitHub Secretsの更新**:
   - GitHubリポジトリの「Settings」>「Secrets」に移動します。
   - 使用しているGCPのサービスアカウントキーの秘密を更新します。

4. **GitHub Actionsのワークフローを再実行**:
   - 正しいキーを使用してワークフローを再実行します。

これらの手順を実行した後も問題が解消しない場合、ワークフローの設定やスクリプトに問題がある可能性があります。その場合、具体的なワークフローの内容や設定を確認する必要があります。