# Tsukureview つくレビュー  
このプロジェクトは筑波大学学生有志「半分、青い。」による匿名掲示板SNSサービス( https://github.com/half-blue/A_plus_Tsukuba )を派生させたプロジェクトです。

## 概要
つくレビューは大学の授業を履修すればよいか悩む問題を解決したい筑波大生向けの授業レビューサイトです。似たようなサイト「みんなのキャンパス」とは違い、会員にならなくても口コミを閲覧できる点や投稿者のリアルな感想・成績等をもとに授業履修の方針を立てることができる点がつくレビューの特徴です。

## サービスのURL
なし

## ライセンス等
プロジェクトに含まれるファイルの内`kdb.json`は
[Make-IT-TSUKUBA](https://github.com/Make-IT-TSUKUBA)
さんが公開している[kdb.json](https://github.com/Make-IT-TSUKUBA/alternative-tsukuba-kdb/blob/master/src/kdb.json)をMPL-2.0 licenseのもとで利用しております。

## 環境構築
1. 必要パッケージの用意
```
pip install -r requirements.txt
```

2. manage.pyが置いてあるディレクトリ(TsukuReview)に入りバッチファイルでマイグレーション・DBに初期データ追加を行います。
```
cd TsukuReview
init.bat
```
※バッチファイルが上手く動作しなかったとき用コマンド  
```
python manage.py makemigrations
python manage.py migrate
python init/add_kdb.py
```

3. スーパーユーザー作成  
以下の情報を画面に従って入力します。
```
email : hoge@piyo.com
password : tsukureview
```

4. スーパーユーザーの名前を設定  
```
python manage.py runserver
```
で起動し、`admin/`にアクセスしログインします。作成したユーザー名に`tsukureview`を設定したら初期設定は完了です。



