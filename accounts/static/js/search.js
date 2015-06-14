
var searchXmlhttp;

function createxmlhttp(){
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
}

function addURLParam(url, name, value){
    url += (url.indexOf("?") == -1 ? "?" : "&")
    url += encodeURIComponent(name) + "=" + encodeURIComponent(value);
    return url;
}

function send_request(url, id){
    value = document.getElementById(id).value;
    createxmlhttp();
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            document.getElementById("searchPrompt").innerHTML=xmlhttp.responseText;
        }
    }
    url = addURLParam(url, "m", value);
    xmlhttp.open("get", url, true);
    xmlhttp.send();
}

