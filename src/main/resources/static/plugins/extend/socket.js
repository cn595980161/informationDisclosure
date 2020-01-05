layui.define(["jquery"], function (a) {
    "use strict";
    var c, b = layui.jquery, d = function () {
    }, e = function () {
        try {
            var a = new WebSocket(d.config.wsUrl);
            return a.onmessage = function (a) {
                d.config.onmessage(a), g.reset()
            }, a.onclose = function () {
                d.config.onclose(), f()
            }, a.onerror = function () {
                d.config.onerror(), f()
            }, a.onopen = function () {
                d.config.onopen(), g.start()
            }, a
        } catch (b) {
            f()
        }
    }, f = function () {
        return d.config.lockReconnect ? void 0 : (d.config.lockReconnect = !0, 1 == d.config.ShInt ? !1 : (setTimeout(function () {
            d.config.isqidong = !1, console.log("服务器重新连接中...."), layui.socket.init(d.config), d.config.lockReconnect = !1
        }, 2e3), void 0))
    }, g = {
        timeoutObj: null, serverTimeoutObj: null, reset: function () {
            d.config.isqidong = !0, console.log("心跳"), clearTimeout(this.timeoutObj), clearTimeout(this.serverTimeoutObj), g.start()
        }, start: function () {
            var a = this;
            this.timeoutObj = setTimeout(function () {
                d.config.isqidong = !0, 1 == c.readyState && c.send(d.config.heartBeat), a.serverTimeoutObj = setTimeout(function () {
                    d.config.isqidong = !1, c.close()
                }, d.config.timeout)
            }, d.config.timeout)
        }
    };
    d.prototype.heartCheck = {
        start: function () {
            g.start()
        }, reset: function () {
            g.reset()
        }
    }, d.prototype.config = {
        wsUrl: "", ShInt: "0", lockReconnect: !1, heartBeat: '{"type":"heartBeat"}', onopen: function () {
            console.log("服务器已连接")
        }, onmessage: function () {
            console.log("收到消息....")
        }, onerror: function () {
            console.log("服务错误")
        }, onclose: function () {
            console.log("服务已关闭")
        }
    }, d.prototype.init = function (a) {
        var f = this;
        return d.config = b.extend({}, f.config, d.config, a), c = e()
    }, d.prototype.close = function () {
        clearTimeout(g.timeoutObj), clearTimeout(g.serverTimeoutObj), d.config.ShInt = 1, c.close()
    }, d.prototype.send = function (a) {
        c.send(a)
    }, a("socket", new d)
});