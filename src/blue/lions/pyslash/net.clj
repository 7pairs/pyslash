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

(ns blue.lions.pyslash.net
  (:require [org.httpkit.client :as http]))

(import '(javax.net.ssl SNIHostName))

(defn- sni-configurer
  [ssl-engine uri]
  (let [ssl-parameters (.getSSLParameters ssl-engine)]
    (.setServerNames ssl-parameters [(SNIHostName. (.getHost uri))])
    (.setSSLParameters ssl-engine ssl-parameters)))

(defn request-html
  [url]
  (let [client (http/make-client {:ssl-configurer sni-configurer})]
    (:body @(http/get url {:client client}))))
