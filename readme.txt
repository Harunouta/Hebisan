【はじめに】
このソフトウェアはとても不親切です。
それでもDLしてくださり、ありがとうございます。
ソースコードの更新を計画しているため、もしgithubのこのリポジトリをみて更新していたらご活用いただけると幸いです。

【このソフトウェアは？】
https://github.com/Harunouta/Sudachi_acc_dic　の辞書を用いて、
Voicevox用にテキストを音声に変換するGUIアプリケーションです。
上記辞書の作成者（作成というよりくっつけただけ）とこのアプリの開発者は同一人物です。

【動かすにあたり】
1.Voicevoxが必要です。このソフトウェアを立ち上げる前にVoicevoxの起動が必要です。

2.以下のライブラリを使用しています。
(全てpipから)
Package            Version
------------------ ---------
ginza              5.1.2
ja-ginza           5.1.2
requests           2.31.0
spacy              3.4.4
spacy-legacy       3.0.12
spacy-loggers      1.0.4
SudachiDict-full   20230110
SudachiPy          0.6.7

【動かし方】
1.別途、Sudachi用ユーザー辞書が必要です。
https://github.com/Harunouta/Sudachi_acc_dic　に記載のアクセント辞書をDLしてください。
2.Ginzaの設定を参照してSudachiのユーザー辞書（Sudachi_acc.dic）を使う設定を行なって下さい。
https://megagonlabs.github.io/ginza/developer_reference.html
3.コマンドラインで
$ test-sc.py 　（windows用に音を鳴らしたい場合は$ test-sc-for-win.py）
と実行してください。
4.音声は再生後、test-sc.py およびtest-sc-for-win.py　と同じ階層のディレクトリに格納されています。

【連絡先】
Twitter(X):@Harunouta_sh