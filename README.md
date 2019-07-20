## 最適な読書体験をしたい
　課題感、アマゾンなどでレコメンドされる本を上から見ていても読書体験がそんなに良くない。
　本の売り上げランキングなどは、大衆に受ける本がほとんどであり、少々独特なセンスを持つ人たちにはそんなに受けが良くない。
　-> 現状の解決策がSNSや人づてに聞き及ぶぐらいしかない（あとジャケ買い）
 
　どうあるべきかを考えるとき、仮に他人の本棚を知ることができれば、集合知と機械学習を用いて自分に向いているだろう本をレコメンドさせることができる

## 会社の技術共有会の小話で話した話

<div>
<iframe src="https://onedrive.live.com/embed?cid=ECE5548EEB0F5802&amp;resid=ECE5548EEB0F5802%21115549&amp;authkey=ALWlrWJS0n3WgPM&amp;em=2&amp;wdAr=1.7777777777777777" width="1186px" height="691px" frameborder="0">これは、<a target="_blank" href="https://office.com/webapps">Office Online</a> の機能を利用した、<a target="_blank" href="https://office.com">Microsoft Office</a> の埋め込み型のプレゼンテーションです。</iframe>
</div>

## Matrix Factorization
　1990年台のNetflix Prizeからある伝統的な手法で、シンプルで動作が早く、ユーザが多くアイテムの数がとても多いときに有効な手法です。  
 
  DeepLearningでも実装できるし、sklearnなどでも関数が用意されています。  
<div align="center">
 <img width="100%" src="https://user-images.githubusercontent.com/4949982/61576638-529b0780-ab17-11e9-9a83-ae2a5b7bea26.png">
</div>
　
## 自分のクエリとなる特徴量
　自分のAmazon Fionaという特定のURLにアクセスると自分の今までKindleで買ってきた本がAjaxでレンダリングされます。   
　Ajaxにより描画されていて、かつ、とても描画が遅いので普通の方法では自動取得できなく、google-chrome-headlessブラウザ等を利用してJSを実行しながら内容を取得できるようにします。  
 - **購入した本の一覧が見えるページ**: https://amazon.co.jp/gp/digital/fiona/manage

**実行コマンド**
```console
$ EMAIL=gim.kobayashi@gmail.com PASSWORD=***** python3 A001_from_kindle.py 
```

<div align="center">
 <img width="400px" src="https://user-images.githubusercontent.com/4949982/61576073-ec5eb680-ab0f-11e9-9ad1-7467191d2929.png">
 <div> fionaのURLをアクセスするとAjaxでこのように描画される </div>
</div>

## いろいろな人達の本棚の特徴量
　レコメンドを行うには大量のデータが必要になります。   
　他人の本棚が必要になるが、`https://booklog.jp/` が本棚SNSになっているのでこれを利用します。  
 (すいません、スクレイピングしないと学習できないので、集めます)  
**実行コマンド**
```console
$ cd DataCollection
$ python3 A001_scrape.py
```
 
　現在120万ユーザが登録しているらしく、8万ユーザの本棚をサンプルして、本棚に登録されている本をウェイトを1として、読んでない本を0とすると、巨大な疎行列を作ることができます。scipyのlil_matrixという疎行列ライブラリを利用して構築すると、400Mbyte程度に収めることだできます。  

<div align="center">
 <img width="100%" src="https://user-images.githubusercontent.com/4949982/61576109-8c1c4480-ab10-11e9-8a80-c7166466c2af.png">
</div>

**実行コマンド**
```console
$ cd MakeBookReadMatrix
$ python3 A001.py
$ python3 B001.py
$ python3 C001.py
```

## 学習
一応、Matrix Factorizationにも過学習という概念があるので、2%をtestとして切り出して、ホールドアウトで、レコメンドしたときのMatrixとのMean Square Errorを小さくします。  
**実行コマンド**
```console
$ cd MakeBookReadMatrix
$ python3 D001.py --fit
fit non-negative matrix factorization
(1757, 1133108)
test mse = 0.000107 # <- 今回のデータ・セットではこのくらい
```

## 推論
 Kindle Fionaから得られた本を、1*BOOK_NUMのMatrixに変形して、学習で作ったモデルに入力すると、各アイテム毎のレコメンドを行った際のウェイトを知ることができる。 

## 結果
 TODO:書きつける
 
## まとめ
　自分の知識や体験の幅を広げるには、レコメンドでウェイトが付いているが、リコールを高めに見たときに低いウェイトの方に来ている本を読むと世界や価値観の広がりを高めることができているように思う。
これは読書家が本の好き嫌いによらずに何かの賞をとった本を上から順番に読んでいくことで、自らの知識の幅を広げることから来ている。 
