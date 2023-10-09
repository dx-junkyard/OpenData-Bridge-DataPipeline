# 対象となるOpenDataを指定するYAMLファイルについて
./opendata.yml に処理対象とするOpenDataの名前やURL、Converterなどを指定してゆきます。  
YAMLフォーマットなので、プロパティは順不同です。また、プラパティは勝手に増やしてもらって構いません。  

## 必須項目
``````
link:
- name: "Tenki"
  title: "テスト"
  url:  "https://www.data.jma.go.jp/developer/xml/feed/regular.xml"
``````

`link:` 全体を一つの要素として読み込むため先頭に必要です。    
`name:` プログラム内部での識別子にですので必ず英数文字で入れてください。他と重複もできません。   
`title:` Webページに表示するオープンデータの名称です。  
`url:` OpenDataの読み出し元です。Curl文字列。  

