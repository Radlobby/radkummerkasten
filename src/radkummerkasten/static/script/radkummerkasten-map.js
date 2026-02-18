/* globals */
/* eslint-disable object-shorthand, object-curly-newline, no-multi-assign, consistent-this, radix, no-global-assign, no-native-reassign */
/* eslint no-console: "warn" */
/* eslint max-depth: ["warn", 6] */
/* eslint no-unused-vars: ["error", { "vars": "local" } ] */

;(function (R) {
    "use strict"

    var that

    R.Map = function (options) {
        that = this

        const defaultOptions = {
            container: "map",
            style: "/static/maps/combined-root.json",
            bearing: 0,
            pitch: 15,
            zoom: 14.5,
            center: [16.3659, 48.1998],
            minZoom: 7,
            maxZoom: 16.9,
        }

        options = { ...defaultOptions, ...options }
        this._options = options

        this._init()
    }

    R.Map.prototype._init = function() {
        let map = new maplibregl.Map(
            that._options,
        )
        that.map = map
    }

}(window.R || (window.R = {})))
