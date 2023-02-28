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

(ns blue.lions.pyslash.util-test
  (:require [clojure.test :refer [deftest is testing]]
            [blue.lions.pyslash.util :as util]))

(deftest test-for-index-of
  (testing "条件に合致する要素がコレクション内にひとつだけ存在する場合、その要素のインデックスを返すこと。"
    (is (= (util/index-of #(= % "栗山") ["栗山" "中村" "外崎" "源田"]) '(0))))
  (testing "条件に合致する要素がコレクション内に複数存在する場合、すべての要素のインデックスを返すこと。"
    (is (= (util/index-of #(re-find #"[中|外]" %1) ["栗山" "中村" "外崎" "源田"]) '(1 2))))
  (testing "条件に合致する要素がコレクション内に存在しない場合、空のリストを返すこと。"
    (is (= (util/index-of #(= % "西口") ["栗山" "中村" "外崎" "源田"]) '()))))
