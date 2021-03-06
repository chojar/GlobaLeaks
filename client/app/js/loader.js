var isBrowserCompatible = function() {
  var crawlers = [
    "Googlebot",
    "Bingbot",
    "Slurp",
    "DuckDuckBot",
    "Baiduspider",
    "YandexBot",
    "Sogou",
    "Exabot",
    "ia_archiver"
  ];

  for (var i=0; i < crawlers.length; crawlers++) {
    if (navigator.userAgent.indexOf(crawlers[i]) !== -1) {
      return true;
    }
  }

  if (typeof window === "undefined") {
    return false;
  }

  if (!(window.File && window.FileList && window.FileReader)) {
    return false;
  }

  if (typeof Blob === "undefined" ||
      (!Blob.prototype.slice && !Blob.prototype.webkitSlice && !!Blob.prototype.mozSlice)) {
    return false;
  }
 
  return true;
};

if (!isBrowserCompatible()) {
  document.getElementById("BrowserSupported").style.display = "none";
  document.getElementById("BrowserNotSupported").style.display = "block";
} else {
  var script = document.createElement("script");
  script.setAttribute("type", "text/javascript");
  script.setAttribute("src", "js/scripts.js");
  document.getElementsByTagName("body")[0].appendChild(script);
}
