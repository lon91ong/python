// 全局变量
var etApp=wps.EtApplication()
var claSel = "";  //保存班级信息

//切换窗口时触发的事件
function OnWindowActivate() {
    console.log("OnWindowActivate" + "=======================");

    var l_doc = wps.EtApplication().ActiveWorkbook;
    SetCurrDocEnvProp(l_doc); // 设置当前文档对应的用户名
    showOATab(); // 根据文件是否为OA文件来显示OA菜单再进行刷新按钮
    setTimeout(activeTab, 500); // 激活页面必须要页签显示出来，所以做1秒延迟
    return;
}

/**
 *  作用：判断OA文档是否被另存为了
 */
function CheckIfOADocSaveAs(doc) {
    if (!doc) {
        return;
    }
    // 获取OA文档的原始保存路径
    var l_Path = GetDocParamsValue(doc, "SourcePath");
    // 原路径和当前文件的路径对比
    return l_Path == doc.FullName;
}


// 当文件保存前触发的事件
function OnWorkbookBeforeSave(doc) {
    console.log("OnWorkbookBeforeSave");

    //设置变量，判断是否当前用户按了自定义的OA文件保存按钮
    var l_IsOADocButtonSave = false;
    l_IsOADocButtonSave = wps.PluginStorage.getItem("OADocUserSave");

    //根据传入参数判断当前文档是否能另存为，默认不能另存为
    if (pCheckCurrOADocCanSaveAs(doc) == false) { //先根据OA助手的默认设置判断是否允许OA文档另存为操作
        //如果配置文件：OA文档不允许另存为，则再判断
        //2、判断当前OA文档是否不落地文档
        if (pIsOnlineOADoc(doc) == true) {
            //如果是不落地文档，则判断是否是系统正在保存
            if (l_IsOADocButtonSave == false) {
                alert("来自OA的不落地文档，禁止另存为本地文档！");
                //如果是OA文档，则禁止另存为
                wps.ApiEvent.Cancel = true;
            }
        } else {
            //这里要再判断OA文档是否被用户另存为
            if (l_IsOADocButtonSave == false) {
                doc.Save(); //直接保存本地就行
                //如果是OA文档，则禁止另存为
                wps.ApiEvent.Cancel = true;
            } else {}
        }

    }

    //保存文档后，也要刷新一下Ribbon按钮的状态
    showOATab();
    return;
}


//文档保存前关闭事件
/**
 * 作用：
 * @param {*} doc 
 */
function OnWorkbookBeforeClose(doc) {
    console.log('OnWorkbookBeforeClose');

    var l_fullName = doc.FullName;
    var l_bIsOADoc = false;
    l_bIsOADoc = CheckIfDocIsOADoc(doc); //判断是否OA文档要关闭
    if (l_bIsOADoc == true) { // OA文档不做处理
        doc.Close(false)
        return;
    }
    //判断是否只读的文档，或受保护的文档，对于只读的文档，不给予保存提示
    if (pISOADocReadOnly(doc) == false) {
        if (doc.Saved == false) { //如果OA文档关闭前，有未保存的数据
            if (wps.confirm("系统文件有改动，是否提交后关闭？" + "\n" + "确认后请按上传按钮执行上传操作。取消则继续关闭文档。")) {
                wps.ApiEvent.Cancel = true;
                return;
            }
        }
    }
    doc.Close(false); //保存待定的更改。
    closeEtIfNoDocument(); // 判断文件个数是否为0，若为0则关闭组件
    if (l_bIsOADoc == true) {
        wps.FileSystem.Remove(l_fullName);
    }
}


//文档保存后关闭事件
function OnWorkbookAfterClose(doc) {
    console.log("OnWorkbookAfterClose");

    var l_NofityURL = GetDocParamsValue(doc, "notifyUrl");
    if (l_NofityURL) {
        l_NofityURL = l_NofityURL.replace("{?}", "3"); //约定：参数为3则文档关闭
        console.log("" + l_NofityURL);
        NotifyToServer(l_NofityURL);
    }

    pRemoveDocParam(doc); // 关闭文档时，移除PluginStorage对象的参数
    pSetetAppUserName(); // 判断文档关闭后，如果系统已经没有打开的文档了，则设置回初始用户名
}

//文档打开事件
function OnWorkbookOpen(doc) {
    var wb = etApp.ActiveWorkbook;
    if (etApp.Workbooks.Count == 1){
        etApp.WindowState = etApp.xlNormal;
        etApp.Width = 600;
    }
    //cellSel = etApp.ActiveCell.Address()
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            //var data = JSON.parse(this.responseText);
            let classes = this.responseText;
            // we get the returned data
            //console.log(classes);
            //console.log(classes.length)
            //console.log(wb.Sheets.Item("成绩录入").Range("B1").Value2)
            //console.log(wps.xlValidateList,wps.xlValidAlertStop, wps.xlEqual)
            wb.Sheets.Item("成绩录入").Unprotect();
            //wb.Sheets.Item("成绩录入").Range("K2").Validation.Delete();
            wb.Sheets.Item("成绩录入").Range("K2").Validation.Add(3, 1, 3, classes);
            wb.Sheets.Item("成绩录入").Protect();
            wb.Sheets.Item("直录").Unprotect();
            //wb.Sheets.Item("直录").Range("K2").Validation.Delete();
            wb.Sheets.Item("直录").Range("B1").Validation.Add(3, 1, 3, classes);
            wb.Sheets.Item("直录").Protect();
        }
        // end of state change: it can be after some time (async)
    };
    xhr.open("GET","http://127.0.0.1:8001/classes",true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Client', 'Excel');
    xhr.send()
    
    //设置当前新增文档是否来自OA的文档
    if (wps.PluginStorage.getItem("IsInCurrOADocOpen") == false) {
        //如果是用户自己在WPS环境打开文档，则设置非OA文档标识
        pSetNoneOADocFlag(doc);
    }

    OnWindowActivate();
    ChangeOATabOnDocOpen(); //打开文档后，默认打开Tab页

}

//新建文档事件
function OnWorkbookNew(doc) {
    //设置当前新增文档是否来自OA的文档
    if (wps.PluginStorage.getItem("IsInCurrOADocOpen") == false) {
        //如果是用户自己在WPS环境打开文档，则设置非OA文档标识
        pSetNoneOADocFlag(doc);
    }
    ChangeOATabOnDocOpen(); // 打开OA助手Tab菜单页
    wps.ribbonUI.Invalidate(); // 刷新Ribbon按钮的状态
}

//活动表格变化
function OnSheetActivate(Sh) {
    claSel = (Sh.Name == "成绩录入"? Sh.Range("K2").Item(1).Value2 : Sh.Range("B1").Item(1).Value2);
}

//表格选区变化事件
var cellSel = ""; //保存变化前的选区
var l_RowUsed = 5;  //使用行数
function OnSelectionChange(Sh, rg) {
    if((Sh.Name == "成绩录入" && cellSel == "$K$2:$L$2") || (Sh.Name == "直录" && cellSel == "$B$1:$C$1")){
        //console.log(rg.Item(1).Value2)
        if (claSel != Sh.Range(cellSel).Item(1).Value2){
            claSel = Sh.Range(cellSel).Item(1).Value2
            //取名单填表
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    var allStu = JSON.parse(this.responseText);
                    //console.log(this.responseText)
                    //console.log([typeof(allStu),allStu.length])
                    l_RowUsed = allStu.length+5
                    //console.log(allStu[1].id)
                    Sh.Unprotect();
                    Sh.Range("A5:C50").ClearContents()
                    for(var i=0;i<allStu.length;i++){
                        Sh.Range("A"+String(i+5)).Value2 = allStu[i].id
                        Sh.Range("B"+String(i+5)).Value2 = allStu[i].name
                        if(Sh.Name == "直录" && allStu[i].score != null){
                            Sh.Range("C"+String(i+5)).Value2 = allStu[i].score
                        }
                    }
                    Sh.Protect();
                }
                // end of state change: it can be after some time (async)
            };
            //console.log(claSel);
            xhr.open("GET","http://10.0.18.207:8001/class?"+encodeURIComponent(claSel),true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('Client', 'Excel');
            xhr.send()
            if(Sh.Name=="成绩录入"){
                Sh.Range("D5:J50").ClearContents()
            }
            Sh.Range("C5").Select();
            //wps.PluginStorage.setItem("RowUsed",l_RowUsed);
        }
    }
    cellSel = rg.Address()
    //etApp.StatusBar=cellSel.split('$')[2]
    //选区边界自动跳转
    if(Number(cellSel.split('$')[2])==l_RowUsed && l_RowUsed>5){
        if(cellSel.split('$')[1]=="J" || Sh.Name=="直录"){
            Sh.Range("C5").Select();
        }else{
            etApp.ActiveCell.Offset(-1*(l_RowUsed-5),1).Select();
        }
    }
    if(Number(cellSel.split('$')[2])<l_RowUsed && l_RowUsed>5){
        if(Sh.Name == "成绩录入" && cellSel.split('$')[1]<"K"){
            Sh.Range("M2").Value2 = etApp.WorksheetFunction.Max(Sh.Range("L5:L50"));
            Sh.Range("M3").Value2 = etApp.WorksheetFunction.Min(Sh.Range("L5:L50"));
        }
        if(Sh.Name == "直录" && cellSel.split('$')[1]=="C"){
            Sh.Range("D1").Value2 = etApp.WorksheetFunction.Max(Sh.Range("C5:C50"));
            Sh.Range("D2").Value2 = etApp.WorksheetFunction.Min(Sh.Range("C5:C50"));
        }
    }
}


/**
 *  作用：判断当前文档是否是只读文档
 *  返回值：布尔
 */
function pISOADocReadOnly(doc) {
    if (!doc) {
        return false;
    }
    var l_openType = GetDocParamsValue(doc, "openType"); // 获取OA传入的参数 openType
    if (l_openType == "") {
        return false;
    }
    try {
        if (!!l_openType.protectType) {
            return true;
        } // 保护
    } catch (err) {
        return false;
    }
}


/**
 *  作用：根据当前活动文档的情况判断，当前文档适用的系统参数，例如：当前文档对应的用户名称等
 */
function SetCurrDocEnvProp(doc) {
    if (!doc) return;
    var l_bIsOADoc = false;
    l_bIsOADoc = pCheckIfOADoc(doc);

    //如果是OA文件，则按OA传来的用户名设置WPS   OA助手WPS用户名设置按钮冲突
    if (l_bIsOADoc == true) {
        var l_userName = GetDocParamsValue(doc, "userName");
        if (l_userName != "") {
            wps.EtApplication().UserName = l_userName;
            return;
        }
    }
    //如果是非OA文件或者参数的值是空值，则按WPS安装默认用户名设置
    wps.EtApplication().UserName = wps.PluginStorage.getItem("WPSInitUserName");
}

/*
    入口参数：doc
    功能说明：判断当前文档是否能另存为本地文件
    返回值：布尔值true or false
*/
function pCheckCurrOADocCanSaveAs(doc) {
    //如果是非OA文档，则允许另存为
    if (CheckIfDocIsOADoc(doc) == false) return true;

    //对于来自OA系统的文档，则获取该文档对应的属性参数
    var l_CanSaveAs = GetDocParamsValue(doc, "CanSaveAs");

    //判断OA传入的参数
    if (typeof (l_CanSaveAs) == "boolean") {
        return l_CanSaveAs;
    }
    return false;
}

/**
 * 作用：判断文档关闭后，如果系统已经没有打开的文档了，则设置回初始用户名
 */
function pSetetAppUserName() {
    //文档全部关闭的情况下，把WPS初始启动的用户名设置回去
    if (wps.EtApplication().Workbooks.Count == 1) {
        var l_strUserName = wps.PluginStorage.getItem("WPSInitUserName");
        wps.EtApplication().UserName = l_strUserName;
    }
}

/**
 * 作用：文档关闭后，删除对应的PluginStorage内的参数信息
 * 返回值：没有返回值
 * @param {*} doc 
 */
function pRemoveDocParam(doc) {
    if (!doc) return;
    wps.PluginStorage.removeItem(doc.FullName);
    return;
}

/**
 * 作用：判断当前文档是否从OA来的文档，如果非OA文档（就是本地新建或打开的文档，则设置EnumOAFlag 标识）
 * 作用：设置非OA文档的标识状态
 * @param {*} doc 
 * 返回值：无
 */
function pSetNoneOADocFlag(doc) {
    if (!doc) return;
    var l_param = wps.PluginStorage.getItem(doc.FullName); //定义JSON文档参数
    var l_objParams = new Object();
    if (l_param) {
        l_objParams = JSON.parse(l_param);
    }
    l_objParams.isOA = EnumOAFlag.DocFromNoOA; // 新增非OA打开文档属性
    wps.PluginStorage.setItem(doc.FullName, JSON.stringify(l_objParams)); // 存入内存中
}


/**
 * 作用：根据设置判断打开文件是否默认激活OA助手工具Tab菜单
 * 返回值：无
 */
function ChangeOATabOnDocOpen() {
    var l_ShowOATab = true; //默认打开
    l_ShowOATab = wps.PluginStorage.getItem("ShowOATabDocActive");

    if (l_ShowOATab == true) {
        if (wps.ribbonUI)
            wps.ribbonUI.ActivateTab("WPSWorkExtTab"); //新建文档时，自动切换到OA助手状态
        else
            wps.ActivateTab("WPSWorkExtTab"); //新建文档时，自动切换到OA助手状态
    }
}