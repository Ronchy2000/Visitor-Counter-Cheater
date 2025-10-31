function getOS() {  //判断所处操作系统
    var sUserAgent = navigator.userAgent.toLowerCase();
    var isWin = (navigator.platform == 'Win32') || (navigator.platform == 'Win64') || (navigator.platform == 'wow64');
    var isMac = (navigator.platform == 'Mac68K') || (navigator.platform == 'MacPPC') || (navigator.platform == 'Macintosh') || (navigator.platform == 'MacIntel');
    if (isMac) return "Mac";
    var isUnix = (navigator.platform == 'X11') && !isWin && !isMac;
    if (isUnix) return "Unix";
    var isLinux = (String(navigator.platform).indexOf("Linux") > -1);
    var bIsAndroid = sUserAgent.toLowerCase().match(/android/i) == "android";
    if (isLinux) {
        if (bIsAndroid) return "Android";
        else return "Linux";
    }
    if (isWin) {

        var isWin2K = sUserAgent.indexOf("Windows nt 5.0") > -1 || sUserAgent.indexOf("Windows NT 5.0") > -1 || sUserAgent.indexOf("Windows 2000") > -1;
        if (isWin2K) return "Win2000";
        var isWinXP = sUserAgent.indexOf("Windows nt 5.1") > -1 || sUserAgent.indexOf("Windows NT 5.1") > -1 || sUserAgent.indexOf("Windows XP") > -1 ||
            sUserAgent.indexOf("Windows XP") > -1;
        if (isWinXP) return "WinXP";
        var isWin2003 = sUserAgent.indexOf("Windows nt 5.2") > -1 || sUserAgent.indexOf("Windows NT 5.2") > -1 || sUserAgent.indexOf("Windows 2003") > -1;
        if (isWin2003) return "Win2003";
        var isWinVista = sUserAgent.indexOf("Windows nt 6.0") > -1 || sUserAgent.indexOf("Windows NT 6.0") > -1 || sUserAgent.indexOf("Windows Vista") > -1;
        if (isWinVista) return "WinVista";
        var isWin7 = sUserAgent.indexOf("Windows nt 6.1") > -1 || sUserAgent.indexOf("Windows 7") > -1 || sUserAgent.indexOf("Windows NT 6.1") > -1;
        if (isWin7) return "Win7";
        var isWin8 = sUserAgent.indexOf("windows nt 6.2") > -1 || sUserAgent.indexOf("windows NT 6.2") > -1 || sUserAgent.indexOf("Windows 8") > -1;
        if (isWin8) return "Win8";
        var isWin10 = sUserAgent.indexOf("windows nt 10.0") > -1 || sUserAgent.indexOf("windows NT 10.0") > -1 || sUserAgent.indexOf("Windows 10") > -1;
        if (isWin10) return "Win10";
    }
    return "其他";
}

function getDigits() { //判断当前操作系统的版本号
    var sUserAgent = navigator.userAgent.toLowerCase();
    var is64 = sUserAgent.indexOf("win64") > -1 || sUserAgent.indexOf("wow64") > -1;
    if (is64) {
        return "64位";
    } else {
        return "32位";
    }
}

function getBrowser() {  // 获取浏览器名
    var rMsie = /(msie\s|trident\/7)([\w\.]+)/;
    var rTrident = /(trident)\/([\w.]+)/;
    var rEdge = /(chrome)\/([\w.]+)/;//IE

    var rFirefox = /(firefox)\/([\w.]+)/;  //火狐
    var rOpera = /(opera).+version\/([\w.]+)/;  //旧Opera
    var rNewOpera = /(opr)\/(.+)/;  //新Opera 基于谷歌
    var rChrome = /(chrome)\/([\w.]+)/; //谷歌
    var rUC = /(chrome)\/([\w.]+)/;//UC
    var rMaxthon = /(chrome)\/([\w.]+)/;//遨游
    var r2345 = /(chrome)\/([\w.]+)/;//2345
    var rQQ = /(chrome)\/([\w.]+)/;//QQ
    var rSafari = /version\/([\w.]+).*(safari)/;

    var ua = navigator.userAgent.toLowerCase();


    var matchBS, matchBS2;

    //IE 低版
    matchBS = rMsie.exec(ua);
    if (matchBS != null) {
        matchBS2 = rTrident.exec(ua);
        if (matchBS2 != null) {
            switch (matchBS2[2]) {
                case "4.0":
                    return {
                        browser:
                            "Microsoft IE",
                        version: "IE: 8"  //内核版本号
                    };
                    break;
                case "5.0":
                    return {
                        browser:
                            "Microsoft IE",
                        version: "IE: 9"
                    };
                    break;
                case "6.0":
                    return {
                        browser:
                            "Microsoft IE",
                        version: "IE: 10"
                    };
                    break;
                case "7.0":
                    return {
                        browser:
                            "Microsoft IE",
                        version: "IE: 11"
                    };
                    break;
                default:
                    return {
                        browser:
                            "Microsoft IE",
                        version: "Undefined"
                    };
            }
        } else {
            return {
                browser: "Microsoft IE",
                version: "IE:" + matchBS[2] || "0"
            };
        }
    }
    //IE最新版
    matchBS = rEdge.exec(ua);
    if ((matchBS != null) && (!(window.attachEvent))) {
        return {
            browser: "Microsoft Edge",
            version: "Chrome/" + matchBS[2] || "0"
        };
    }
    //UC浏览器
    matchBS = rUC.exec(ua);
    if ((matchBS != null) && (!(window.attachEvent))) {
        return {
            browser: "UC",
            version: "Chrome/" + matchBS[2] || "0"
        };
    }
    //火狐浏览器
    matchBS = rFirefox.exec(ua);
    if ((matchBS != null) && (!(window.attachEvent))) {
        return {
            browser: "火狐",
            version: "Firefox/" + matchBS[2] || "0"
        };
    }
    //Oper浏览器
    matchBS = rOpera.exec(ua);
    if ((matchBS != null) && (!(window.attachEvent))) {
        return {
            browser: "Opera",
            version: "Chrome/" + matchBS[2] || "0"
        };
    }
    //遨游
    matchBS = rMaxthon.exec(ua);
    if ((matchBS != null) && (!(window.attachEvent))) {
        return {
            browser: "遨游",
            version: "Chrome/" + matchBS[2] || "0"
        };
    }
    //2345浏览器
    matchBS = r2345.exec(ua);
    if ((matchBS != null) && (!(window.attachEvent))) {
        return {
            browser: "2345",
            version: "Chrome/ " + matchBS[2] || "0"
        };
    }
    //QQ浏览器
    matchBS = rQQ.exec(ua);
    if ((matchBS != null) && (!(window.attachEvent))) {
        return {
            browser: "QQ",
            version: "Chrome/" + matchBS[2] || "0"
        };
    }
    //Safari（苹果）浏览器
    matchBS = rSafari.exec(ua);
    if ((matchBS != null) && (!(window.attachEvent)) && (!(window.chrome)) && (!(window.opera))) {
        return {
            browser: "Safari",
            version: "Safari/" + matchBS[1] || "0"
        };
    }
    //谷歌浏览器
    matchBS = rChrome.exec(ua);
    if ((matchBS != null) && (!(window.attachEvent))) {
        matchBS2 = rNewOpera.exec(ua);
        if (matchBS2 == null) {
            return {
                browser: "谷歌",
                version: "Chrome/" + matchBS[2] || "0"
            };
        } else {
            return {
                browser: "Opera",
                version: "opr/" + matchBS2[2] || "0"
            };
        }
    }
    return {
        browser: "未知浏览器",
        version: "未知操作系统"
    };
}
function    _tsites_updateVisit_() {
	var pathname = window.location.pathname;
    var hosts= window.location.host;
    var browser = getBrowser().browser || "未知浏览器";
    var OS = getOS() + " " + getDigits() || "未知操作系统";
    var clickimg = new Image();
    var vp = "";
    try{
        if(undefined != visite_record_collect_params && visite_record_collect_params.length>0){
            vp = visite_record_collect_params;
        }
    }catch (e){
    }
    clickimg.src = "/system/resource/tsites/click.jsp?lc="+encodeURIComponent(pathname)+"&hosts="+encodeURIComponent(hosts)+"&ac=updateVisit&vp="+encodeURIComponent(vp)+"&os="+encodeURIComponent(OS)+"&bs="+encodeURIComponent(browser);
}
var _jsq_image = new Image();
function _jsq_encode(){_keyStr="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";this.encode=function(a){if(a==null||a==undefined||a=="")return"";var b=new Array();var c,chr2,chr3;var d,enc2,enc3,enc4;var i=0;a=_utf8_encode(a);while(i<a.length){c=a[i++];chr2=a[i++];chr3=a[i++];d=c>>2;enc2=((c&3)<<4)|(chr2>>4);enc3=((chr2&15)<<2)|(chr3>>6);enc4=chr3&63;if(isNaN(chr2)){enc3=enc4=64}else if(isNaN(chr3)){enc4=64}b.push(_keyStr.charAt(d)+_keyStr.charAt(enc2)+_keyStr.charAt(enc3)+_keyStr.charAt(enc4))}return escape(b.join(''))};_utf8_encode=function(a){a=a.replace(/\r\n/g,"\n");var b=new Array();var d=0;for(var n=0;n<a.length;n++){var c=a.charCodeAt(n);if(c<128){b[d++]=c}else if((c>127)&&(c<2048)){b[d++]=(c>>6)|192;b[d++]=(c&63)|128}else{b[d++]=(c>>12)|224;b[d++]=((c>>6)&63)|128;b[d++]=(c&63)|128}}return b}}
function _jsq_(treeid, pagename, newsid, owner)
{
    if(window.top != window)
        return;
      _tsites_updateVisit_();   
        
    var c = navigator.appName=='Netscape'?screen.pixelDepth:screen.colorDepth;
    var e = new _jsq_encode();
    var r = '&e=1&w='+screen.width + '&h='+ screen.height+'&treeid='+treeid+'&refer='+e.encode(document.referrer)+ '&pagename='+e.encode(pagename)+'&newsid='+newsid;
    _jsq_image.src = "/system/resource/code/datainput.jsp?owner="+owner+ r;
}




