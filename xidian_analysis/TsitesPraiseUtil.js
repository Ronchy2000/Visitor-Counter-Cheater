function TsitesPraiseUtil() {
    var _this = this;
    _this.nodeid;
    _this.iscanclickidobj;
    _this.imageid;
    _this.apptype = "";
    _this.basenum = 0;
    _this.uid = "";
    _this.homepageid = 0;
    _this.contentid = 0;
    _this.pdtype = 1;
    _this.nodeObj = null;
    _this.isCanclickidobj = null;
    _this.action = "/system/resource/tsites/praise.jsp";
    _this.praiseNum = 0;
    _this.praiseing = false;
    _this.limttype = 'allpage';
    _this.limithour = 24;
    _this.setParam = function (param) {
        _this.nodeid = param.nodeid ? param.nodeid : 0;
        _this.iscanclickidobj = param.iscanclickidobj ? param.iscanclickidobj : 0;
        _this.apptype = param.apptype ? param.apptype : "";
        _this.basenum = param.basenum ? param.basenum : 0;
        _this.uid = param.uid ? param.uid : 0;
        _this.homepageid = param.homepageid ? param.homepageid : 0;
        _this.contentid = param.contentid ? param.contentid : 0;
        _this.imageid = param.imageid ? param.imageid : 0;
        _this.limttype = param.limttype ? param.limttype : 'allpage';
        _this.pdtype = param.pdtype ? param.pdtype : 1;
        _this.limithour = param.limithour ? param.limithour : 24;
        if (_this.nodeid) {
            _this.nodeObj = jQuery("#" + _this.nodeid);
        }
        if (_this.iscanclickidobj) {
            _this.isCanclickidobj = jQuery("#" + _this.iscanclickidobj);
        }
        jQuery.ajax({
            url: "/system/resource/js/jquery/jquery.cookie.js",
            dataType: "script",
            cache: true
        }).done(function () {
            _this.getPraise();
            _this.bindClickMethod();
        });
    }
    /**
     * 更新一个内容的点赞次数
     */
    _this.updatePraise = function () {
        if (_this.praiseing === true) {
            return;
        }
        _this.praiseing = true;
        var key = "tsites_praise_";
        if (_this.limttype === 'allpage') {
            key += _this.uid;
        } else if (_this.limttype === 'specilpage') {
            key += +_this.uid + "_" + _this.homepageid;
        }
        var al = _this.getCookie(key);
        if (al !== 1) {
            _this.setCookie(key, "1", {path: '/'}, _this.limithour);
            jQuery.post(_this.action, {
                "uid": _this.uid,
                "homepageid": _this.homepageid,
                "apptype": _this.apptype,
                "contentid": _this.contentid,
                "pdtype": _this.pdtype,
                "ac": "updatePraise"
            }, function (data) {
                if(data.result){
                    _this.praiseNum++;
                    $("#" + _this.nodeid).html(_this.praiseNum);
                }
                _this.praiseing = false;
            }, "json");
        }
    }

    /**
     * 查询一个内容点赞次数
     *
     */
    _this.getPraise = function () {
        /**
         * 是否可以进行点赞
         *
         */
        var key = "tsites_praise_";
        if (_this.limttype == 'allpage') {
            key += _this.uid;
        } else if (_this.limttype == 'specilpage') {
            key += +_this.uid + "_" + _this.homepageid;
        }
        var a2 = _this.getCookie(key);
        if (a2 == 1) {
            _this.isCanclickidobj.val("false");
        }

        jQuery.post(_this.action, {
            "uid": _this.uid,
            "homepageid": _this.homepageid,
            "apptype": _this.apptype,
            "contentid": _this.contentid,
            "pdtype": _this.pdtype,
            "basenum": _this.basenum,
            "ac": "getPraise"
        }, function (data) {
            if (_this.nodeObj && data) {
                $("#" + _this.nodeid).html(data.praise);
                _this.praiseNum = data.praise;
            }
        }, "json");
    }

    /**
     * 对点赞对象做事件绑定
     */
    _this.bindClickMethod = function () {
        $("#" + _this.imageid).bind("click", function () {
            _this.updatePraise();
        });
    }
    //得到cookie值
    // Retrieve the value of the cookie with the specified name.
    _this.getCookie = function (sName) {
        // cookies are separated by semicolons
        var aCookie = document.cookie.split("; ");
        for (var i = 0; i < aCookie.length; i++) {
            var aCrumb = aCookie[i].split("=");
            if (sName == aCrumb[0])
                return unescape(aCrumb[1]);
        }
        return null;
    }

    //设置cookie值
    // Create a cookie with the specified name and value.
    // The cookie expires after one year.
    _this.setCookie = function (sName, sValue, path, oh) {
        var expires = "";
        if (oh > 0) {
            var exp = new Date();
            exp.setTime(exp.getTime() + oh * 60 * 60 * 1000);//过期时间
            expires = exp.toGMTString();
        }
        if (expires != "") {
            document.cookie = sName + "=" + escape(sValue) + ";path=" + path.path + ";expires=" + expires;
        } else {
            document.cookie = sName + "=" + escape(sValue) + ";path=" + path.path + ";";
        }
    }
}