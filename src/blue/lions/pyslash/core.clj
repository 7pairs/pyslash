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

(ns blue.lions.pyslash.core
  (:require [clojure.string :as string]
            [net.cgrand.enlive-html :as html]
            [blue.lions.pyslash.net :as net]))

(defn- remove-nbsp
  [target]
  (string/replace target "\u00a0" ""))

(defn- get-formal-team-name
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

(defn- get-root-node
  [html]
  (html/html-snippet html))

(defn- get-teams
  [node]
  (let [card (-> node
                 (html/select [:h4#cardTitle])
                 (first)
                 (:content)
                 (first))
        m (re-find #"^(\S+)\s*対\s*(\S+)$" card)]
    (map #(-> % (remove-nbsp) (get-formal-team-name)) [(m 1) (m 2)])))

(defn- get-date
  [node]
  (let [update-time (-> node
                        (html/select [:p#upDate :span])
                        (first)
                        (:content)
                        (first))]
    (re-find #"^\d+年\d+月\d+日" update-time)))

(defn- get-stadium
  [node]
  (let [data (-> node
                 (html/select [:p.data])
                 (first)
                 (:content)
                 (first))
        m (re-find #"^◇[^◇]+◇[^◇]+◇(\S+)$" data)]
    (m 1)))

(defn- get-round
  [node]
  (let [win-loss (-> node
                     (html/select [:p#time])
                     (first)
                     (:content)
                     (first))
        m (re-find #"(\d+)勝(\d+)敗(\d+)分け$" win-loss)]
    (reduce + (map #(Integer/parseInt %) [(m 1) (m 2) (m 3)]))))

(defn- get-score
  [node]
  (map #(map (fn [x] (first (:content x)))
             (drop-last (drop 1 (html/select % [:td]))))
       (drop 1 (html/select node [:table.scoreTable :tr]))))

(defn- get-pitcher
  [node sign]
  (let [pitcher (first (filter #(= (first (:content (first %))) sign)
                               (map #(html/select % [:td])
                                    (drop 1 (html/select node [:table.pitcher :tr])))))]
    (map #(first (:content %)) [(nth pitcher 1) (nth pitcher 3) (nth pitcher 4) (nth pitcher 5)])))

(defn- get-win
  [node]
  (get-pitcher node "○"))

(defn- get-save
  [node]
  (get-pitcher node "Ｓ"))

(defn- get-lose
  [node]
  (get-pitcher node "●"))

(defn -main
  [& args]
  (let [html (net/request-html (first args))
        root-node (get-root-node html)
        teams (get-teams root-node)
        date (get-date root-node)
        stadium (get-stadium root-node)
        round (get-round root-node)
        score (get-score root-node)
        win (get-win root-node)
        save (get-save root-node)
        lose (get-lose root-node)]
    (println win save lose)))
