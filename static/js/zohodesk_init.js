// static/js/zohodesk_init.js

(function() {
  var d = document;
  var s = d.createElement("script");
  s.type = "text/javascript";
  s.id = "zohodeskasapscript";
  s.defer = true;
  s.nonce = "{place_your_nonce_value_here}";  // Replace dynamically if CSP is enforced
  s.src = "https://desk.zoho.com/portal/api/web/asapApp/514102000032997001?orgId=718674855";
  var t = d.getElementsByTagName("script")[0];
  t.parentNode.insertBefore(s, t);

  window.ZohoDeskAsapReady = function(callback) {
    var asyncCalls = window.ZohoDeskAsap__asyncalls = window.ZohoDeskAsap__asyncalls || [];
    if (window.ZohoDeskAsapReadyStatus) {
      if (callback) asyncCalls.push(callback);
      asyncCalls.forEach(fn => fn && fn());
      window.ZohoDeskAsap__asyncalls = null;
    } else if (callback) {
      asyncCalls.push(callback);
    }
  };
})();
