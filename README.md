# 環境構築
## WSL(1.2.5.0)
vscodeに以下の拡張機能をインストールする  
* WSL  
* SQLite
* Python

左下の<font color="Blue">><</font>からwslに接続を行う  
Ctrl + @ でターミナルを起動  
適当なフォルダを作成し，リポジトリをクローンする  
`git clone https://github.com/Tanakaryuki/FastAPI_APP.git`  

フォルダに移動する  
`cd FastAPI_APP`  

仮想環境の作成  
`python3 -m venv env`  

(仮想環境の作成に失敗した場合)  
`sudo apt install python3.xx-venv`  

仮想環境を有効化  
`. env/bin/activate`  

ライブラリをインストール  
`sudo pip install -r requirement.txt`  

(ライブラリのインストールに失敗した場合)  
`sudo apt install python3-pip`  

<br>

# 開発の開始  
FastAPIの起動  
`uvicorn main:app --reload`  

ブラウザで[http://localhost:8000](http://localhost:8000)を開く  

<br>

# デバッグについて  
SQLiteの閲覧  
vscode上で  
`Ctrl + Shift + p`  
`SQLite: Open Database`  

APIのテスト  
[http://localhost:8000/docs](http://localhost:8000/docs)から行う  

APIドキュメントの確認  
[http://localhost:8000/redoc](http://localhost:8000/redoc)から行う  

<br>

# 開発の終了  
FastAPIの停止  
`Ctrl + c`  

仮想環境の無効化  
`deactivate`  

# インサイダーゲームについて  
## ルール  
1. プレイヤーは「市民」と「インサイダー」に分けられる(インサイダーのみ答えを知っている)  
2. 各プレイヤーはターン毎にChatGPTに質問をする  
3. 質問を終えるとみんなで話し合い答えを決定する  
4. もし答えが合わなかったら全員負けになる  
5. 答えが合ったらインサイダーを投票する  
6. インサイダーを当てた場合「市民」に1点，インサイダーを外した場合「インサイダー」に2点が入る  
7. 全ラウンド終了後に一番点数が高いプレイヤーが勝利  

# アプリ概要  
```mermaid
sequenceDiagram
    autonumber
    actor user1 as ユーザ(参加者)
    actor user as ユーザ(親)
    participant front as Webページ
    participant api as APIサーバ
    participant db as DBサーバ
    participant ai as Chat GPT
    user->>front: Topページアクセス
    user->>front: settingページにRequest
    Note over user1,front: ルーム作成
    front->>user: 詳細設定を表示
    user->>front: 詳細設定を選択
    front->>api: 選択を送信
    api->>db: ルーム情報を登録
    db->>api: 返却
    api->>front: 返却
    front->>user: 待機画面を表示
    user1->>front: 待機画面にRequest
    front->>user1: ユーザ登録を表示
    user1->>front: ユーザ登録
    front->>api: 選択を送信
    api->>db: ルーム情報を確認
    db->>api: 返却
    api->>front:　返却
    front->>user1: 待機画面を表示
    user->>front: ゲーム開始
    front->>api: 選択を送信
    api->>db: ルーム情報を更新
    db->>api: 返却
    api->>front: 返却
    front->>user: プレイ画面を表示
    Note over user1,front: ゲーム開始
    loop ラウンド数
        Note over user1,front: 質問開始
        loop 指定回数
            user->>front:　質問を送信
            front->>api: 質問を送信
            api->>ai: 質問を送信
            ai->>api: 返却
            api->>front: 返却
            front->>user: 返却
        end
        Note over user1,front: 答え合わせ
        user->>front: 答えを選択
        front->>api: 選択を送信
        api->>db: ルーム情報を確認
        db->>api: 返却
        api->>front: 返却
        front->>user: 結果を表示
        opt 答え==お題の時
            Note over user,front: インサイダーを投票
            user->>front: インサイダーを投票
            front->>api: 選択を送信
            api->>db: ルーム情報を確認
            db->>api: 返却
            api->>front: 返却
        end
        front->>user: ラウンド結果を表示
        opt ラウンド終了時
            Note over user,front: 最終結果の発表
            user->>front: 最終結果を表示
            front->>api: 問い合わせ
            api->>db: ルーム情報を確認
            db->>api: 返却
            api->>front: 返却
            front->>user: 最終結果を表示
        end
        
    end
    Note over user1,front: ゲーム終了
```

# 画面遷移  
* home(/)
* ルーム作成(/setting)
* ルーム入室(/{room_id})
* 参加者待機(/waiting/{room_id}?id={user_id})
* ゲームプレイ(/playing/{room_id}?id={user_id})
* 答え合わせ(/answering/{room_id}?id={user_id})
* インサイダー投票(/voting/{room_id}?id={user_id})
* ラウンド結果(/round_result/{room_id})
* 最終結果(/final_result/{room_id})  

ゲームプレイからラウンド結果までは一つにまとめても良い