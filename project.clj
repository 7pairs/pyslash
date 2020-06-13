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

(defproject pyslash "2.0.0"
  :description "Parse and format baseball scores."
  :url "https://github.com/7pairs/pyslash"
  :license {:name "Apache License, Version 2.0"
            :url "https://www.apache.org/licenses/LICENSE-2.0"}
  :dependencies [[org.clojure/clojure "1.10.1"]
                 [enlive "1.1.6"]
                 [http-kit "2.4.0-alpha6"]]
  :profiles {:uberjar {:main pyslash.core, :aot :all}}
  :main pyslash.core
  :repl-options {:init-ns pyslash.core})
