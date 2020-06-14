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

(ns pyslash.core
  (:require [clojure.string :as string]
            [net.cgrand.enlive-html :as html]
            [org.httpkit.client :as http]))

(import '(javax.net.ssl SNIHostName))

(defn sni-configurer
  [ssl-engine uri]
  (let [ssl-parameters (.getSSLParameters ssl-engine)]
    (.setServerNames ssl-parameters [(SNIHostName. (.getHost uri))])
    (.setSSLParameters ssl-engine ssl-parameters)))

(def client (http/make-client {:ssl-configurer sni-configurer}))

(defn add-quote
  [target]
  (str "\\\"" target "\\\""))

(defn remove-nbsp
  [target]
  (string/replace target "\u00a0" ""))

(defn get-formal-name
  [target]
  (case target
    "西武" "埼玉西武"
    "ソフトバンク" "福岡ソフトバンク"
    "楽天" "東北楽天"
    "ロッテ" "千葉ロッテ"
    "日本ハム" "北海道日本ハム"
    "巨人" "読売"
    "ＤｅＮＡ" "横浜ＤｅＮＡ"
    "広島" "広島東洋"
    "ヤクルト" "東京ヤクルト"
    target))

(defn get-root-node
  [response-body]
  (-> response-body
      (html/html-snippet)
      (html/select [:body])))

(defn get-teams
  [node]
  (let [card-title (-> node
                       (html/select [(html/id= (add-quote "cardTitle"))])
                       (first)
                       (html/text))
        m (re-find #"^(\S+)\s*対\s*(\S+)$" card-title)]
    (map #(-> % (remove-nbsp) (get-formal-name)) [(m 1) (m 2)])))

(defn get-date
  [node]
  (let [up-date (-> node
                    (html/select [(html/id= (add-quote "upDate")) :span])
                    (first)
                    (html/text))]
    (re-find #"^\d+年\d+月\d+日" up-date)))

(defn get-stadium
  [node]
  (let [data (-> node
                 (html/select [:p])
                 (html/select [(html/attr= :class (add-quote "data"))])
                 (first)
                 (html/text))
        m (re-find #"^◇[^◇]+◇[^◇]+◇(\S+)$" data)]
    (m 1)))

(defn get-round
  [node]
  (let [time (-> node
                 (html/select [(html/id= (add-quote "time"))])
                 (first)
                 (html/text))
        m (re-find #"(\d+)勝(\d+)敗(\d+)分け$" time)]
    (reduce + (map #(Integer/parseInt %) [(m 1) (m 2) (m 3)]))))

(defn -main
  [& args]
  (let [response-body {:body @(http/get (first args) {:client client})}
        root-node (get-root-node response-body)
        teams (get-teams root-node)
        date (get-date root-node)
        stadium (get-stadium root-node)
        round (get-round root-node)]
    (print round)))
