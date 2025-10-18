/* eslint-disable no-unused-vars, object-shorthand, object-curly-newline, no-multi-assign, consistent-this */
/* eslint no-console: "warn" */

;(function (R) {
    "use strict"

    console.log("Radkummerkasten!")

    document.addEventListener("DOMContentLoaded", function() {
        var radkummerkasten = new R.Map({

        })
        window.radkummerkasten = radkummerkasten
    })  


})(window.R || (window.R = {}))
