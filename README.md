# Tsukureview つくレビュー  
このプロジェクトは筑波大学学生有志「半分、青い。」による匿名掲示板SNSサービス、[A+つくば](https://github.com/half-blue/A_plus_Tsukuba)を派生させたプロジェクトです。

## 概要
つくレビューは大学の授業を履修すればよいか悩むという問題を解決したい筑波大生向けの授業レビューサイトです。競合サイト「みんなのキャンパス」とは違い、会員にならなくても口コミを閲覧できる点や閲覧者が欲しいと思う情報を実際に受講した先輩たちが投稿しているので授業履修の方針を立てやすくなるという点がつくレビューの特徴です。

## サービスのURL
なし

## ライセンス等
プロジェクトに含まれるファイルの内`kdb.json`は
[Make-IT-TSUKUBA](https://github.com/Make-IT-TSUKUBA)
さんが公開している[kdb.json](https://github.com/Make-IT-TSUKUBA/alternative-tsukuba-kdb/blob/master/src/kdb.json)をMPL-2.0 licenseのもとで利用しております。

## 環境構築
1. 仮想環境の構築  
仮想環境を構築し、仮想環境に入ります。仮想環境のフォルダを構築する場所はどこでも構いません。
```
python -m venv env_review
cd env_review/Scripts
activate
```
仮想環境から抜け出す際は`deactivate`とコマンドを打ちます。

2. manage.pyが置いてあるディレクトリ(TsukuReview)に入り、必要なライブラリをインストールしバッチファイルでマイグレーション・DBに初期データ追加を行います。
```
cd TsukuReview
pip install -r requirements.txt
init.bat
```
※バッチファイルが上手く動作しなかったとき用コマンド  
```
python manage.py makemigrations
python manage.py migrate
python manage.py create_database
python manage.py create_superuser
```

3. サーバーの起動  
```
python manage.py runserver
```
でアプリを起動する。



