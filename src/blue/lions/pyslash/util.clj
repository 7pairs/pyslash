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

(ns blue.lions.pyslash.util
  (:require [clojure.string :as string]))

(import '(java.text Normalizer Normalizer$Form))

(defn index-of
  "抽出条件に合致する要素のインデックスを返す。
   @param pred 抽出条件
   @param coll 走査対象のコレクション
   @return 条件に合致する要素のインデックス"
  [pred coll]
  (keep-indexed #(when (pred %2) %1) coll))

(defn remove-nbsp
  [target]
  (string/replace target "\u00a0" ""))

(defn convert-to-half
  [target]
  (Normalizer/normalize target Normalizer$Form/NFKC))
