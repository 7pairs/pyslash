;;;; Copyright 2014-2022 HASEBA Junya
;;;;
;;;; Licensed under the Apache License, Version 2.0 (the "License");
;;;; you may not use this file except in compliance with the License.
;;;; You may obtain a copy of the License at
;;;;
;;;;     http://www.apache.org/licenses/LICENSE-2.0
;;;;
;;;; Unless required by applicable law or agreed to in writing, software
;;;; distributed under the License is distributed on an "AS IS" BASIS,
;;;; WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
;;;; See the License for the specific language governing permissions and
;;;; limitations under the License.

(ns blue.lions.pyslash.core-test
  (:require [clojure.test :refer [deftest is testing]]
            [net.cgrand.enlive-html :as html]
            [blue.lions.pyslash.core :as core]))

(deftest test-for-first-element
  (testing "セレクタにマッチする要素がノード内に存在する場合、その先頭の要素を返すこと。"
    (let [node (html/html-snippet "<!DOCTYPE html>
                                   <html>
                                     <body>
                                       <ul>
                                         <li>栗山</li>
                                         <li>中村</li>
                                         <li>外崎</li>
                                         <li>源田</li>
                                       </ul>
                                     </body>
                                   </html>")]
      (is (= (first (:content (core/first-element node [:ul :li]))) "栗山"))))
  (testing "セレクタにマッチする要素がノード内に存在しない場合、nilを返すこと。"
    (let [node (html/html-snippet "<!DOCTYPE html>
                                   <html>
                                     <body>
                                       <ul>
                                         <li>栗山</li>
                                         <li>中村</li>
                                         <li>外崎</li>
                                         <li>源田</li>
                                       </ul>
                                     </body>
                                   </html>")]
      (is (nil? (core/first-element node [:ol :li]))))))

(deftest test-for-first-content
  (testing "要素内にcontentが存在する場合、先頭のcontentを返すこと。"
    (let [node (html/html-snippet "<!DOCTYPE html>
                                   <html>
                                     <body>
                                       <p>栗山<br>中村<br>外崎<br>源田</p>
                                     </body>
                                   </html>")]
      (is (= (core/first-content (first (html/select node [:p]))) "栗山"))))
  (testing "要素内にcontentが存在しない場合、nilを返すこと。"
    (let [node (html/html-snippet "<!DOCTYPE html>
                                   <html>
                                     <body>
                                       <p>
                                         <img src='https://www.seibulions.jp/cmn/images/player/2022/ph_player01.jpg'>
                                       </p>
                                     </body>
                                   </html>")]
      (is (nil? (core/first-content (first (html/select node [:img]))))))))

(deftest test-formal-team-name
  (testing "埼玉西武ライオンズの正式名称に変換されること。"
    (is (= (core/formal-team-name "西武") "埼玉西武")))
  (testing "オリックスバファローズの正式名称に変換されること。"
    (is (= (core/formal-team-name "オリックス") "オリックス")))
  (testing "福岡ソフトバンクホークスの正式名称に変換されること。"
    (is (= (core/formal-team-name "ソフトバンク") "福岡ソフトバンク")))
  (testing "北海道日本ハムファイターズの正式名称に変換されること。"
    (is (= (core/formal-team-name "日本ハム") "北海道日本ハム")))
  (testing "千葉ロッテマリーンズの正式名称に変換されること。"
    (is (= (core/formal-team-name "ロッテ") "千葉ロッテ")))
  (testing "読売ジャイアンツの正式名称に変換されること。"
    (is (= (core/formal-team-name "巨人") "読売")))
  (testing "中日ドラゴンズの正式名称に変換されること。"
    (is (= (core/formal-team-name "中日") "中日")))
  (testing "横浜ＤｅＮＡベイスターズの正式名称に変換されること。"
    (is (= (core/formal-team-name "ＤｅＮＡ") "横浜ＤｅＮＡ")))
  (testing "阪神タイガースの正式名称に変換されること。"
    (is (= (core/formal-team-name "阪神") "阪神")))
  (testing "広島東洋カープの正式名称に変換されること。"
    (is (= (core/formal-team-name "広島") "広島東洋")))
  (testing "東京ヤクルトスワローズの正式名称に変換されること。"
    (is (= (core/formal-team-name "ヤクルト") "東京ヤクルト")))
  (testing "東北楽天ゴールデンイーグルスの正式名称に変換されること。"
    (is (= (core/formal-team-name "楽天") "東北楽天"))))

(deftest test-for-formal-stadium-name
  (testing "ベルーナドームの正式名称に変換されること。"
    (is (= (core/formal-stadium-name "ベルーナドーム") "ベルーナドーム")))
  (testing "京セラドーム大阪の正式名称に変換されること。"
    (is (= (core/formal-stadium-name "京セラドーム大阪") "京セラドーム大阪")))
  (testing "福岡PayPayドームの正式名称に変換されること。"
    (is (= (core/formal-stadium-name "ペイペイドーム") "福岡PayPayドーム")))
  (testing "札幌ドームの正式名称に変換されること。"
    (is (= (core/formal-stadium-name "札幌ドーム") "札幌ドーム")))
  (testing "ZOZOマリンスタジアムの正式名称に変換されること。"
    (is (= (core/formal-stadium-name "ＺＯＺＯマリン") "ZOZOマリンスタジアム")))
  (testing "東京ドームの正式名称に変換されること。"
    (is (= (core/formal-stadium-name "東京ドーム") "東京ドーム")))
  (testing "バンテリンドームナゴヤの正式名称に変換されること。"
    (is (= (core/formal-stadium-name "バンテリンドーム") "バンテリンドームナゴヤ")))
  (testing "横浜スタジアムの正式名称に変換されること。"
    (is (= (core/formal-stadium-name "横浜スタジアム") "横浜スタジアム")))
  (testing "阪神甲子園球場の正式名称に変換されること。"
    (is (= (core/formal-stadium-name "甲子園") "阪神甲子園球場")))
  (testing "Mazda Zoom-Zoomスタジアム広島の正式名称に変換されること。"
    (is (= (core/formal-stadium-name "マツダスタジアム") "Mazda Zoom-Zoomスタジアム広島")))
  (testing "明治神宮野球場の正式名称に変換されること。"
    (is (= (core/formal-stadium-name "神宮") "明治神宮野球場")))
  (testing "楽天生命パーク宮城の正式名称に変換されること。"
    (is (= (core/formal-stadium-name "楽天生命パーク") "楽天生命パーク宮城"))))

(deftest test-for-yoza
  (testing "「与座」が「與座」に変換されること。"
    (is (= (core/yoza "与座") "與座")))
  (testing "「今井」が変換されないこと。"
    (is (= (core/yoza "今井") "今井"))))
