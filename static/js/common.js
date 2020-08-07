/**
 * Created by tarena on 18-12-10.
 */
function createXhr(){
    var xhr = null
    if(window.XMLHttpRequest){
        xhr = new XMLHttpRequest();
    }else{
        xhr = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xhr;
}
