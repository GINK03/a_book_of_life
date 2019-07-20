## 最適な読書体験をしたい
　アマゾンなどでレコメンドされる本を上から見ていても読書体験がそんなに良くありません。  
　本の売り上げランキングなどは、大衆に受ける本がほとんどであり、少々独特なセンスを持つ人たちにはそんなに受けが良くないです。  
　結果として現状の解決策がSNSや人づてに聞き及ぶぐらいしかないのとジャケ買いなどがせいぜいです  
　どうあるべきかを考えるとき、仮に他人の本棚を知ることができれば、集合知と機械学習を用いて自分に向いているだろう本をレコメンドさせることができます

## 会社の技術共有会の小話で話した話

<div>
<iframe src="https://onedrive.live.com/embed?cid=ECE5548EEB0F5802&amp;resid=ECE5548EEB0F5802%21115549&amp;authkey=ALWlrWJS0n3WgPM&amp;em=2&amp;wdAr=1.7777777777777777" width="100%" height="400px"  frameborder="0">これは、<a target="_blank" href="https://office.com/webapps">Office Online</a> の機能を利用した、<a target="_blank" href="https://office.com">Microsoft Office</a> の埋め込み型のプレゼンテーションです。</iframe>
</div>

## Matrix Factorization
　2000年台のNetflix Prizeからある伝統的な手法で、シンプルで動作が早く、ユーザが多くアイテムの数がとても多いときに有効な手法です。  
 
  DeepLearningでも実装できるし、sklearnなどでも関数が用意されています。  
<div align="center">
 <img width="100%" src="https://user-images.githubusercontent.com/4949982/61576638-529b0780-ab17-11e9-9a83-ae2a5b7bea26.png">
</div>

## コード
[https://github.com/GINK03/a_book_of_life:embed]

## 自分のクエリとなる特徴量
　自分のAmazon Fionaという特定のURLにアクセスると自分の今までKindleで買ってきた本がAjaxでレンダリングされます。   
　Ajaxにより描画されていて、かつ、とても描画が遅いので普通の方法では自動取得できなく、google-chrome-headlessブラウザ等を利用してJSを実行しながら内容を取得できるようにします。  
 - **購入した本の一覧が見えるページ**: https://amazon.co.jp/gp/digital/fiona/manage

**実行コマンド**
```console
$ cd DataCollection
$ EMAIL=*****@gmail.com PASSWORD=***** python3 A001_from_kindle.py 
$ python3 B001_scan_local_html.py
```

<div align="center">
 <img width="400px" src="https://user-images.githubusercontent.com/4949982/61576073-ec5eb680-ab0f-11e9-9ad1-7467191d2929.png">
 <div> fionaのURLをアクセスするとAjaxでこのように描画される </div>
</div>

## いろいろな人達の本棚の特徴量
　レコメンドを行うには大量のデータが必要になります。   
　他人の本棚が必要になりますが、`https://booklog.jp/` が本棚SNSになっているのでこれを利用します。  
 (すいません、スクレイピングしないと学習できないので、集めます)  
**実行コマンド**
```console
$ cd DataCollection
$ python3 A001_scrape.py
```
 
　現在120万ユーザが登録しているらしく、全体の一割程度でいいのでユーザの本棚をサンプルして、本棚に登録されている本を1として、登録されていない本を0とすると、巨大な疎行列を作ることができます。scipyのlil_matrixという疎行列ライブラリを利用して構築すると、400Mbyte程度に収めることができます。  

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
 Kindle Fionaから得られた本を、1*BOOK_NUMのMatrixに変形して、学習で作ったモデルに入力すると、各アイテム毎のレコメンドを行った際のウェイトを知ることができます。 
 
**実行コマンド**
```console
$ python3 D001.py
```
**scores_00.csv** というファイルができ、その中にタイトルとウェイトが記されている.  

## 自分の結果
<div align="center">
 <img width="100%" src="https://user-images.githubusercontent.com/4949982/61576953-d5be5c80-ab1b-11e9-92e7-699bc367f731.png">
 <div> 過去に漫画を大量に買っていたのでおおよそ納得の結果 </div>
</div>
別の絵本が多いユーザでもやってみましたが、絵本が多く上位に出るので想定通りできていることが確認できました。  


## 依存(Ubuntuを想定)
 - **google-chrome**
```console
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo apt install ./google-chrome-stable_current_amd64.deb
```
 - **chrome-driver**
```console
$ wget https://chromedriver.storage.googleapis.com/75.0.3770.140/chromedriver_linux64.zip # google-chromeのversionに応じたものを使ってください
$ unzip chromedriver_linux64.zip
$ sudo mv chromedriver /usr/local/bin/
```
 - **requirements.txt**
```console
$ pip install -r requirements.txt
``` 

### 再現できないときいは
　よく指摘されるので、難しい場合は、私のデータで学習したときのデータからモデルまでの動作が確認できたときのスナップショットがあるので、参考にしてみてください。 

 - https://www.dropbox.com/s/q7sbqqiniqmhbhi/a_book_of_life.tar.gz?dl=0

## まとめ
　自分の知識や体験の幅を広げるには、レコメンドでウェイトが付いているが、リコールを高めに見たときに低いウェイトの方に来ている本を読むと世界や価値観の広がりを高めることができているように思います。  
 商業的にはおそらく高いウェイトの作品をレコメンドするとよいのでしょうが、自分に近すぎるコンテンツということもあり食傷気味であり、Amazonででる本などは興味を惹かれなかったのですが、自分でこのレコメンドエンジンを使う分にはこの制約がなくて良さそうです。  

