var _et = {}

var bUseHttps = false;

function _EtInvoke(funcs) {
    var info = {};
    info.funcs = funcs;
    var func = bUseHttps ? WpsInvoke.InvokeAsHttps : WpsInvoke.InvokeAsHttp
    func(WpsInvoke.ClientType.et, // 组件类型
        "EtOAAssist", // 插件名，与wps客户端加载的加载的插件名对应
        "dispatcher", // 插件方法入口，与wps客户端加载的加载的插件代码对应，详细见插件代码
        info, // 传递给插件的数据
        function (result) { // 调用回调，status为0为成功，其他是错误
            if (result.status) {
                if (bUseHttps && result.status == 100) {
                    WpsInvoke.AuthHttpesCert('请在稍后打开的网页中，点击"高级" => "继续前往"，完成授权。')
                    return;
                }
                alert(result.message)

            } else {
                console.log(result.response)
            }
        })
}

function GetDemoPath(fileName) {

    var url = document.location.host;
    console.log(url);
    return document.location.protocol + "//" + url + "/file/" + fileName;
}

function onlineEditDoc() {
    var filePath = GetDemoPath("成绩录入.xlsx")//prompt("请输入打开文件路径（本地或是url）：", GetDemoPath("成绩录入.xlsx"))
    //var uploadPath = GetUploadPath()//prompt("请输入文档上传路径:", GetUploadPath())

    _EtInvoke([{
        "OnlineEditDoc": {
            "docId": "123", // 文档ID
            //"uploadPath": uploadPath, // 保存文档上传路径
            "fileName": filePath,
            //showButton: "btnSaveFile"
        }
    }])
}

_et['onlineEditDoc'] = {
    action: onlineEditDoc,
    code: _EtInvoke.toString() + "\n\n" + onlineEditDoc.toString(),
    detail: "\n\
  说明：\n\
    点击按钮，输入要打开的文档路径，输入文档上传路径，如果传的不是有效的服务端地址，将无法使用保存上传功能。\n\
    打开演示后,将根据文档路径下载并打开对应的文档，保存将自动上传指定服务器地址\n\
    \n\
  方法使用：\n\
    页面点击按钮，通过wps客户端协议来启动演示组件，调用oaassist插件，执行传输数据中的指令\n\
    funcs参数信息说明:\n\
        OnlineEditDoc方法对应于OA助手dispatcher支持的方法名\n\
            docId 文档ID，OA助手用以标记文档的信息，以区分其他文档\n\
            uploadPath 保存文档上传路径\n\
            fileName 打开的文档路径\n\
            showButton 要显示的按钮\n\
"
}

window.onload = function () {
    document.getElementById("onlineEditDoc").onclick = onlineEditDoc;
}