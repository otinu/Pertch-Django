## どんなアプリ？
**迷子のペットについて情報共有をするアプリケーション**です。<br>
アプリ名は「Pet」+「Search」をかけてます。<br>
元々、Springフレームワークで開発したものをDjangoフレームワークでリプレースしました。

## なぜ作った？
**Djangoフレームワークの学習アウトプットのため**です。<br>
今回はなるべくDjangoに集中したかったため既存の成果物をリプレースする方針にしました。

## こだわった技術

### スリムView
**Viewのコード量をなるべく少なくする**ことを意識しました。<br>
例えばバリデーション処理はViewで記述する予定でしたが、Formクラスを利用することで処理をViewから切り離せるというメリットから**Formクラスを開発途中で導入**しました。

### 検索機能
写真や登録日時などを除いた、**全カラムで複合条件検索**ができる機能を作成しました。<br>
また、検索結果の一覧は**各カラムで昇順・降順ソート**ができ、Formクラスでカバーしきれない**バリデーションをView側でフォロー**するなどの調整もしています。

### 自動テスト
Selenium+ChromドライバーやPlaywrightなどでのUIテストは導入せず、Djangoのデフォルト機能での自動テストを実装しました。<br>
**導入理由**は導入コストと成果物の目的から**早く実装する,バグを減らす**ことを実現したかったためです。<br>
**テストケースは事前にテスト項目書を作成**し、必要なテストを結合テストで網羅しています。

### フロント関連
素のJavaScript(バニラJS)で**自作アニメーション**にチャレンジしました。<br>
その他、**テンプレート継承やフィルタ**など画面周りの開発にはDjango機能を使用しました。

## ギャラリー

**トップ画面** <br>

https://github.com/otinu/Pertch-Django/assets/65097619/3f471a62-490c-4381-9296-30212ef8ddd2

**一覧画面**
![image](https://github.com/otinu/Pertch-Django/assets/65097619/a595a0b8-9ba2-462e-9161-548e495c6309)



**登録画面**
![image](https://github.com/otinu/Pertch-Django/assets/65097619/3a2da97c-350a-4b12-99a7-0a6ded9dd381)


**ペット詳細画面**
![image](https://github.com/otinu/Pertch-Django/assets/65097619/2792abef-a236-46b5-9cbe-e49f0237923c)








## 開発環境

- OS：Ubuntu(22.04.3)
- 言語：HTML, CSS, Sass, JavaScript, Python
- フレームワーク：Django
- JS ライブラリ：jQuery, zipcloud(郵便番号API)
- IDE：VSCode

**pip list**
```
Package                   Version
------------------------- ------------
asgiref                   3.7.2
attrs                     23.1.0
certifi                   2023.7.22
charset-normalizer        3.3.0
Django                    3.2.21
django-currentuser        0.6.1
exceptiongroup            1.1.3
greenlet                  2.0.2
idna                      3.4
iniconfig                 2.0.0
jsonschema                4.19.1
jsonschema-specifications 2023.7.1
mypy                      1.5.1
mypy-extensions           1.0.0
packaging                 23.2
Pillow                    10.0.1
pip                       23.2.1
pluggy                    1.3.0
pyee                      9.0.4
pytz                      2023.3.post1
referencing               0.30.2
rpds-py                   0.10.3
setuptools                59.6.0
sqlparse                  0.4.4
text-unidecode            1.3
tomli                     2.0.1
typing_extensions         4.7.1
urllib3                   2.0.6
```

## 設計書関連
- テーブル定義書
- 画面遷移図
- ER図
- テスト項目書
- レイアウトイメージ図

ご覧いただく場合、お手数ですが下記テキストファイル記載のURLよりアクセスをお願い致します。<br>
[draw.io](./Pertch_draw.io_.txt)

その際、画面右下部に編集ボタン(ペンアイコン)が表示されます。クリックすると、draw.ioが起動します。<br>
&ensp;※1.編集後に保存しようとするとご自身のドライブやローカルに保存されます。<br>
&ensp;※2.draw.ioで起動するにはGoogleアカウントが必要になります。


![image](https://github.com/otinu/Pertch-Django/assets/65097619/e3272306-2a44-4f35-a40d-1b2b13c6bb2c)

