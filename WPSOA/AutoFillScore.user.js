// ==UserScript==
// @name         AutoFillScore
// @namespace    http://tampermonkey.net/
// @version      0.2
// @description  Fill the scores automatically
// @author       Xiaoniu29
// @match        http://211.81.249.99/js_main.aspx?xh=*
// @require      https://s3.pstatp.com/cdn/expire-1-M/jquery/1.12.4/jquery.min.js
// @grant        none
// ==/UserScript==

var svrIP = "127.0.0.1"; //服务器IP
var col = 5; //期末:5,总评:7

var claName = ''; //保存班级名称
var quRes = []; //保存服务器返回的结果
var sTable = []; //页面表单
var None = null; //适配python的定义

const insP = document.querySelector('#headDiv > ul');
const exeNode = document.createElement("li")
const clsNode = document.createElement("li")
exeNode.class = "top";
clsNode.class = "top";
exeNode.innerHTML = '<a class="top_link"><span> 执行填表</span></a>';
clsNode.innerHTML = '<a class="top_link"><span> 清空表单</span></a>';
var execBtn = insP.insertBefore(exeNode, insP.lastElementChild.nextSibling);
var clsBtn = insP.insertBefore(clsNode, insP.lastElementChild.nextSibling);
execBtn.style.display="none"; //暂不显示
clsBtn.style.display='none';
execBtn.addEventListener("click", execFill, true);
clsBtn.addEventListener("click", clsForm, true);
const iframe = document.getElementById("frame_content");

(function() {
    'use strict';

    const launchReq = async (reqcmd) => {
        const headers = new Headers({
            "Content-Type": "application/json",
            "Client": "Greasemonkey",
            "Access-Control-Allow-Origin": '*',
        });
        const response = await fetch(new Request(reqcmd, {method: 'GET', headers: headers}));
        return response.json();
    }
    iframe.onload = function() {
        var tempNode = $('#TextBox1', iframe.contentDocument);
        if(tempNode.length) { //存在
            tempNode[0].value = "5678";
            tempNode = $('#Button1', iframe.contentDocument);
            if (tempNode.length && tempNode[0].value == "确  定") {
                tempNode[0].click();
            }else{
                try {
                    claName = $('#ddlBJMC > option:nth-child(1)', iframe.contentDocument)[0].attributes.value.nodeValue;
                    sTable = $('#DataGrid1', iframe.contentDocument)[0];
                    if($('#Button1', iframe.contentDocument).length == 0){ //是否已有保存按钮
                        var saveNode = document.createElement("span"); 
                        saveNode.innerHTML='<input type="submit" name="Button1" value="保  存" id="Button1" class="button" />';
                        var saveParent = $('.footbutton',iframe.contentDocument)[0];
                        saveParent.insertBefore(saveNode, saveParent.childNodes[0]); 
                    }
                    execBtn.style.display="block"; //显示按钮
                    clsBtn.style.display="block";
                    $('#rad_4', iframe.contentDocument)[0].click(); //关闭自动保存
                    console.log('Class found:' + claName);
                } catch (err) {
                    console.log('Class not found!\n' + err.message);
                    execBtn.style.display="none"; //不是填表页，隐藏按钮
                    clsBtn.style.display="none";
                }
                if (claName != '') {
                    //想要直接把Promise的返回值赋给quRes，需要用IIFE包装一下async/await才行
                    (async ()=>{quRes = await launchReq('http://'+svrIP+':8001/class?'+encodeURI(claName));})();
                    //setTimeout(()=>{console.log(quRes);},1000);
                }
            }
        }
    };
})();

function execFill() {
    var n = 0;
    for (var i = 1; i < sTable.rows.length; i++) { //排除表头行
        var idnum = sTable.rows[i].cells[1].innerText.replace(/(\s|\u00A0)+$/,'');//排除空白取学号
        if(quRes[idnum] != null){
            $(".text_nor.width68", sTable.rows[i].cells[col])[0].value = quRes[idnum];
        }else{ //没成绩
            if(idnum.slice(0,2)<claName.slice(-4,-2)){
                console.info(sTable.rows[i].cells[2].innerText + "-降级!");
                $("select", sTable.rows[i].cells[8])[0].options[0].selected = true;
            }else{
                console.info(sTable.rows[i].cells[2].innerText + "-缺考!");
                $("select", sTable.rows[i].cells[8])[0].options[1].selected = true;
            }
        }
    }
    $('#Button1', iframe.contentDocument)[0].click(); //保存
};

function clsForm(){
    for (var i = 1; i < sTable.rows.length; i++) { //排除表头行
        $(".text_nor.width68", sTable.rows[i].cells[col])[0].value =''; //清空期末成绩
        $("select", sTable.rows[i].cells[8])[0].options[2].selected = true;
    }
    $('#Button4', iframe.contentDocument)[0].click(); //清空总评成绩
};
