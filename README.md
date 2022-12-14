# jpPostcodeDB

郵便番号から、都道府県や市区町村、町域を調べるpythonのプログラムです。

郵便局公式HPからcsvデータをダウンロードし、sqlite3のDBを作成しています。最終更新日から月が変わった場合、もしくは1ヵ月以上経過している場合は自動的に情報を更新します。

## How to use
```
$ python3 jpPostcode.py 1000005
(1000005, '東京都', 'ﾄｳｷｮｳﾄ', '千代田区', 'ﾁﾖﾀﾞｸ', '丸の内（次のビルを除く）', 'ﾏﾙﾉｳﾁ(ﾂｷﾞﾉﾋﾞﾙｦﾉｿﾞｸ)')
```

※ 標準のライブラリのみで作成しているため、ライブラリのインストールや仮想環境の作成は必要ありません。

DBが存在しなかった場合は、自動でDBを作成します。ネットワークの速度に依存しますが、恐らく1秒以内にDB生成は終了します。生成または更新だけを単体で行いたい場合には、郵便番号をつけずに実行してください。

また、同じ郵便番号に複数の町域が含まれる場合があります。その場合、標準出力には複数行出力されます。

強制的に更新したい場合は、`jpPostcode.db`を削除すれば自動的に一から生成されます。

## DBを単体で利用したい場合

sqlite3を利用したDBの中身は、下記のような構造になっています。

```
postcodes(
    id integer PRIMARY KEY AUTOINCREMENT,
    postcode integer NOT NULL,
    prefecture text NOT NULL,
    prefecture_kana text NOT NULL,
    municipalities text NOT NULL,
    municipalities_kana text NOT NULL,
    town_area text NOT NULL,
    town_area_kana text NOT NULL,
    unique(postcode, prefecture, municipalities, town_area)
);
```

利用する際は、下記のようなコードで検索できます。なお、SQLを利用するだけではDBの更新は行われません。

```
SELECT * FROM postcodes where postcode = 1000005;
```

## LICENCE
CC0

商用利用、個人利用、改変、二次配布、全てにおいてフリーです。何の制限もありません。自由に使ってください。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)
