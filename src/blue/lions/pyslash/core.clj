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

(ns blue.lions.pyslash.core
  (:require [clojure.string :as string]
            [net.cgrand.enlive-html :as html]
            [blue.lions.pyslash.net :as net]
            [blue.lions.pyslash.util :as util]))

;;; Enlive用ヘルパー関数

(defn first-element
  "セレクタの条件にマッチするノード内の先頭の要素を返す。
   @param node 検索対象のノード
   @param selector 抽出条件のセレクタ
   @return 条件にマッチした先頭の要素"
  [node selector]
  (first (html/select node selector)))

(defn first-content
  "要素内の先頭の{@code content}を返す。
   @param element 要素
   @return 先頭の{@code content}"
  [element]
  (first (:content element)))

;;; 表記変換用ヘルパー関数

(defn formal-team-name
  "チームの正式名称を返す。
   @param target チーム名の新聞表記
   @return チームの正式名称"
  [target]
  (case target
    "西武" "埼玉西武"
    "ソフトバンク" "福岡ソフトバンク"
    "日本ハム" "北海道日本ハム"
    "ロッテ" "千葉ロッテ"
    "巨人" "読売"
    "ＤｅＮＡ" "横浜ＤｅＮＡ"
    "広島" "広島東洋"
    "ヤクルト" "東京ヤクルト"
    "楽天" "東北楽天"
    target))

(defn formal-stadium-name
  "球場の正式名称を返す。
   @param target 球場名の新聞表記
   @return 球場の正式名称"
  [target]
  (case target
    "ペイペイドーム" "福岡PayPayドーム"
    "ＺＯＺＯマリン" "ZOZOマリンスタジアム"
    "バンテリンドーム" "バンテリンドームナゴヤ"
    "横浜" "横浜スタジアム"
    "甲子園" "阪神甲子園球場"
    "マツダスタジアム" "Mazda Zoom-Zoomスタジアム広島"
    "神宮" "明治神宮野球場"
    "楽天生命パーク" "楽天生命パーク宮城"
    target))

(defn yoza
  "與座の表記を旧字体に変換する。
   @param target 選手名の新聞表記
   @return 変換後の選手名"
  [target]
  (if (= target "与座") "與座" target))

(defn remove-nbsp 
  [target]
  (string/replace target "\u00a0" ""))

(defn- get-root-node
  [html]
  (html/html-snippet html))

(defn- get-teams
  [node]
  (let [card (-> node
                 (first-element [:h4#cardTitle])
                 (first-content))
        match (re-find #"^(\S+)\s*対\s*(\S+)$" card)]
    (map #(-> % (util/remove-nbsp) (formal-team-name)) [(match 1) (match 2)])))

(defn- get-date
  [node]
  (let [update-time (-> node
                        (first-element [:p#upDate :span])
                        (first-content))]
    (re-find #"^\d+年\d+月\d+日" update-time)))

(defn- get-stadium
  [node]
  (let [data (-> node
                 (first-element [:p.data])
                 (first-content))
        match (re-find #"^◇[^◇]+◇[^◇]+◇([^◇]+)" data)]
    (formal-stadium-name (match 1))))

(defn- get-round
  [node]
  (let [win-loss (-> node
                     (first-element [:p#time])
                     (first-content))
        match (re-find #"(\d+)勝(\d+)敗(\d+)分け$" win-loss)]
    (reduce + (map #(Integer/parseInt %) [(match 1) (match 2) (match 3)]))))

(defn- get-score
  [node]
  (map #(map (fn [x] (first-content x))
             (drop-last (drop 1 (html/select % [:td]))))
       (drop 1 (html/select node [:table.scoreTable :tr]))))

(defn- get-pitcher
  [node sign]
  (let [pitcher (first (filter #(= (first-content (first %)) sign)
                               (map #(html/select % [:td])
                                    (drop 1 (html/select node [:table.pitcher :tr])))))]
    (map #(when-let [reslut (first-content %)] (util/convert-to-half reslut))
         [(nth pitcher 1) (nth pitcher 3) (nth pitcher 4) (nth pitcher 5)])))

(defn- get-win
  [node]
  (get-pitcher node "○"))

(defn- get-save
  [node]
  (get-pitcher node "Ｓ"))

(defn- get-lose
  [node]
  (get-pitcher node "●"))

(defn- get-homerun-ininngs
  [table top-bottom]
  (let [ininngs (map #(-> % (first-content) (util/remove-nbsp) (util/convert-to-half))
                     (drop 9 (html/select (first-element table [:tr]) [:th])))]
    (map #(str (nth ininngs %) "回" top-bottom)
         (flatten (map #(util/index-of (fn [x] (re-find #".本" (first-content x)))
                                       (drop 9 (html/select % [:td])))
                       (drop 1 (html/select table [:tr])))))))

(defn- get-homeruns
  [node]
  (let [tables (html/select node [:table.batter])
        homerun-ininngs (sort #(compare %1 %2)
                              (flatten [(get-homerun-ininngs (first tables) "表")
                                        (get-homerun-ininngs (last tables) "裏")]))
        homeruns (map #(-> % (first-content) (util/convert-to-half))
                      (html/select (filter #(= (first-content (first-element % [:dt])) "◇本塁打")
                                           (html/select node [:dl.data])) [:dd]))
        matches (map #(re-find #"^(\D+)(\d+)号\((ソロ|2ラン|3ラン|満塁)\d+m=([^\)]+)\)$" %) homeruns)]
    (map #(vector %1 (%2 1) (%2 2) (%2 3) (%2 4)) homerun-ininngs matches)))

(defn- pad-right
  [target filler]
  (let [max-length (apply max (map #(count %) target))]
    (map #(str % (string/join (take (- max-length (count %)) (repeat filler)))) target)))

(defn- format-score
  [target]
  (string/join "  " (map #(string/join " " %) (partition 3 target))))

(defn- calc-run
  [target]
  (reduce + (map #(try
                    (Integer/parseInt %)
                    (catch Exception _
                      0)) target)))

(defn- gen-pitcher
  [result]
  (str (nth result 0) "勝" (nth result 1) "敗" (nth result 2) "Ｓ"))

(defn- output
  [data]
  (let [base-top-team (last (:teams data))
        base-bottom-team (first (:teams data))
        [bottom-team top-team] (pad-right (:teams data) "\u3000")
        top-score (format-score (first (:score data)))
        bottom-score (format-score (last (:score data)))
        top-run (calc-run (first (:score data)))
        bottom-run (calc-run (last (:score data)))
        [win lose save] (pad-right (map #(yoza %)
                                        (remove nil? [(first (:win data)) (first (:lose data)) (first (:save data))])) "\u3000")
        win-result (gen-pitcher (drop 1 (:win data)))
        save-result (gen-pitcher (drop 1 (:save data)))
        lose-result (gen-pitcher (drop 1 (:lose data)))]
    (println (str "【" base-bottom-team " vs " base-top-team " 第" (:round data) "回戦】"))
    (println (str "（" (:date data) "／" (:stadium data) "）"))
    (println)
    (println (str top-team "  " top-score "  " top-run))
    (println (str bottom-team "  " bottom-score "  " bottom-run))
    (println)
    (when win (println (str "[勝] " win " " win-result)))
    (when save (println (str "[Ｓ] " save " " save-result)))
    (when lose (println (str "[敗] " lose " " lose-result)))
    (println)
    (when (not-empty (:homeruns data))
      (println "[本塁打]")
      (doseq [homerun (:homeruns data)] (println (str "  " (homerun 0) " " (homerun 1) " " (homerun 2) "号 " (homerun 3) " （" (yoza (homerun 4)) "）"))))))

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
        lose (get-lose root-node)
        homeruns (get-homeruns root-node)]
    (output {:teams teams :date date :stadium stadium :round round :score score :win win :save save :lose lose :homeruns homeruns})))
