# img_trimmer
画像の四角を自動抽出してトリミングするプログラム

## 使い方
### 基本的な使い方
dataフォルダにトリミングしたい画像を入れておく。  
trim.pyを起動すると順に処理され、resultフォルダに処理結果の画像が保存される

### 注意
2値化にthresholdを使っている。パラメータ調節が必要

### 改善
Cannyとか使って、直線っぽいものを検出したほうがいいかもしれない。

## サンプル
### 入力
<img src="https://github.com/Penguin8885/img_trimmer/blob/master/sample/input.JPG" alt="サンプル画像" title="サンプル画像">

### 出力
<img src="https://github.com/Penguin8885/img_trimmer/blob/master/sample/output.JPG" alt="サンプル画像" title="サンプル画像">
