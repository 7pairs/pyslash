; Copyright 2014-2020 HASEBA Junya
;
; Licensed under the Apache License, Version 2.0 (the "License");
; you may not use this file except in compliance with the License.
; You may obtain a copy of the License at
;
;     http://www.apache.org/licenses/LICENSE-2.0
;
; Unless required by applicable law or agreed to in writing, software
; distributed under the License is distributed on an "AS IS" BASIS,
; WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
; See the License for the specific language governing permissions and
; limitations under the License.

(ns blue.lions.pyslash.core-test
  (:require [clojure.test :refer [deftest is testing]]
            [blue.lions.pyslash.core :as core]))

(deftest test-get-formal-team-name
  (testing "埼玉西武ライオンズ"
    (is (= (core/get-formal-team-name "西武") "埼玉西武")))
  (testing "福岡ソフトバンクホークス"
    (is (= (core/get-formal-team-name "ソフトバンク") "福岡ソフトバンク")))
  (testing "東北楽天ゴールデンイーグルス"
    (is (= (core/get-formal-team-name "楽天") "東北楽天")))
  (testing "千葉ロッテマリーンズ"
    (is (= (core/get-formal-team-name "ロッテ") "千葉ロッテ")))
  (testing "北海道日本ハムファイターズ"
    (is (= (core/get-formal-team-name "日本ハム") "北海道日本ハム")))
  (testing "オリックスバファローズ"
    (is (= (core/get-formal-team-name "オリックス") "オリックス")))
  (testing "読売ジャイアンツ"
    (is (= (core/get-formal-team-name "巨人") "読売")))
  (testing "横浜ＤｅＮＡベイスターズ"
    (is (= (core/get-formal-team-name "ＤｅＮＡ") "横浜ＤｅＮＡ")))
  (testing "阪神タイガース"
    (is (= (core/get-formal-team-name "阪神") "阪神")))
  (testing "広島東洋カープ"
    (is (= (core/get-formal-team-name "広島") "広島東洋")))
  (testing "中日ドラゴンズ"
    (is (= (core/get-formal-team-name "中日") "中日")))
  (testing "東京ヤクルトスワローズ"
    (is (= (core/get-formal-team-name "ヤクルト") "東京ヤクルト"))))

(deftest test-yoza
  (testing "与座"
    (is (= (core/yoza "与座") "與座")))
  (testing "ニール"
    (is (= (core/yoza "ニール") "ニール"))))
