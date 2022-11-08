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

(ns blue.lions.pyslash.util-test
  (:require [clojure.test :refer [deftest is testing]]
            [blue.lions.pyslash.util :as util]))

(deftest test-index-of
  (testing "存在"
    (is (= (util/index-of #(= % "山川") ["栗山" "岡田" "山川" "山野辺" "外崎"]) (list 2))))
  (testing "非存在"
    (is (= (util/index-of #(= % "源田") ["栗山" "岡田" "山川" "山野辺" "外崎"]) (list)))))
