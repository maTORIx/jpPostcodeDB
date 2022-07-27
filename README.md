# jpPostcodeDB

郵便番号から、都道府県や市区町村、町域を調べるpythonのプログラムです。

郵便局公式HPからcsvデータをダウンロードし、sqlite3のDBを作成しています。最終更新日から月が変わった場合、もしくは1ヵ月以上経過している場合は自動的に情報を更新します。

## How to use
```
$ python3 jpPostcode.py 1000005
(1000005, '東京都', 'ﾄｳｷｮｳﾄ', '千代田区', 'ﾁﾖﾀﾞｸ', '丸の内（次のビルを除く）', 'ﾏﾙﾉｳﾁ(ﾂｷﾞﾉﾋﾞﾙｦﾉｿﾞｸ)')
```

※ 標準のライブラリのみで作成しているため、ライブラリのインストールや仮想環境の作成は必要ありません。

## LICENCE
CC0

商用利用、個人利用、改変、二次配布、全てにおいてフリーです。何の制限もありません。自由に使ってください。
