function getVersion()
{
    var browser=navigator.appName;
    var b_version=navigator.appVersion;
    var version=b_version.split(";");
    var trim_Version=version[1].replace(/[ ]/g,"");
    return (browser=="Microsoft Internet Explorer" && trim_Version=="MSIE10.0");
}

function ImageScale(uid, width, height, zoomtype, zoomout)
{
    var _this = this; // 把this保存下来，以后用_this代替this，这样就不会被this弄晕了

    _this.imgs = new Array(); // 图片组
    _this.urls = new Array(); // 链接组
    _this.titles = new Array(); // 标题组
    
    
    // 图片加载完毕事件
    _this.onimgload = function(targetid,loadIndex)
    {
        _this.imgs[loadIndex].setAttribute("loadedflag", true);
        _this.constrainimg(document.getElementById(uid+targetid + "pic"), _this.imgs[loadIndex]);
    }   
    
    // 添加图片
    _this.addimg = function(imgsrc, url, title,targetid)
    {
        var imgcount = _this.imgs.length;
        _this.imgs[imgcount] = new Image();
        
        _this.imgs[imgcount].onload = function(){_this.onimgload(targetid,imgcount)};
        
        _this.imgs[imgcount].src = imgsrc;
        
        _this.urls[imgcount] = url;
        _this.titles[imgcount] = title;
    }

    // 等比例设置图片
    _this.constrainimg = function(imgobj, imagevar)
    {
        try
        {
            var widthrate = imagevar.width / width;
            var heightrate = imagevar.height / height;
            var imgwidth = 0;
            var imgheight = 0;
            if(widthrate > 1 || heightrate > 1) // 图片过大时
            {
                if(zoomtype)// 按比例缩小
                {
                    var rate = Math.max(widthrate, heightrate);
                    imgwidth = Math.max(1, Math.min(imagevar.width/rate, width));
                    imgheight = Math.max(1, Math.min(imagevar.height/rate, height));
                }
                else// 拉伸
                {
                    imgwidth = width;
                    imgheight = height;
                }
            }
            else if(widthrate < 1 || heightrate < 1) // 图片小
            {
                if(false)// 自动放大
                {
                    if(zoomtype)// 按比例放大
                    {
                        var rate = Math.max(widthrate, heightrate);
                        imgwidth = Math.max(1, Math.min(imagevar.width/rate, width));
                        imgheight = Math.max(1, Math.min(imagevar.height/rate, height));
                    }
                    else // 拉伸
                    {
                        imgwidth = width;
                        imgheight = height;
                    }
                }
                else
                {
                   imgwidth = imagevar.width;
                   imgheight = imagevar.height;
                }
            }
            else // 大小合适
            {
               imgwidth = width;
               imgheight = height;
            }

            imgobj.src = imagevar.src;
            imgobj.width = imgwidth;
            imgobj.height = imgheight;
            //imgdiv.style.paddingTop = (height - imgheight)/2;
        }
        catch(e)
        {
        }
    }
}