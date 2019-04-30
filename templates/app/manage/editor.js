function log(text){console.log(text);}

function copyHtml(src,tar){
    var html=src.html();
    tar.val(html);
}
function copyText(src,tar){
    var text=src.val();
    tar.html(text);
}
function initEditableSwitch(){
    var edit_toobar=$('#edit-toolbar');
    var btn=$('.switch-editable');
    var btn_ilz=new SwitchInitializer(btn);
    var tar1=btn_ilz.tar1;var tar2=btn_ilz.tar2;
    var sw=new Switch(btn,()=>{
        tar1.attr('contenteditable','true');
    },
    ()=>{
        tar1.attr('contenteditable','false');
        var sw_dv=switches.doubleview[0];log(switches)
        sw_dv.easyTurnOff();
    });
    switches['editable']=[];
    switches.editable.push(sw);
}
//----------------cmd---------------//
function checkCmd(text){
    if(text.length<4)return false;
    else if(text.slice(0,2)!="::")return false;
    text=text.slice(2,text.length).toLowerCase();
    return text;
}
function executeCmd(cmd){
    var sw=switches.editable[0];
    var btn=$('#btn-editable');
    if(cmd=='edit'){
        show(btn);
        sw.easyTurnOn();
        return true;
    }
    else if(cmd=='exit'){
        sw.easyTurnOff();
        return true;
    }
    else return false;
}
function initCommandButton(){
    var btn=$('.cmd-btn');
    var input=$('.cmd-input');
    var msg_box=$('.msg-box-tem');
    btn.unbind().click((e)=>{
        var cmd=input.val();
        cmd=checkCmd(cmd);
        if(! cmd){showMsg(msg_box,'命令错误')}
        else {
            success=executeCmd(cmd);
            if(success){
               input.val('');
            }
            else showMsg(msg_box,'命令错误');
        };
    });
    input.keydown((e)=>{
        if(e.keyCode==13){hideMsg(msg_box);btn.click();}

    })
}
//--------------gather blog info-----------------//
function gatherBlogInfo(){
    var title=$('#title-input').val();
    var cate=$('#category-input').val();
    var tags=$('#tags-input').val().split(';');
    var md=$('#text-input').val();
    var msg_box=$('.msg-box-tem');
    if(title.trim()==''){showMsg(msg_box,'标题不能为空！');return false;}
    if(cate.trim()==''){showMsg(msg_box,'目录不能为空！');return false;}
    if(md.trim()==''){showMsg(msg_box,'文章不能为空');return false;}
    var json={title:title,category:cate,tags:tags,md:md};
    return json
}
//----------end cmd-----------//
function initSwitchTest(){
    initEditableSwitch();
    initCommandButton();
    initSwitch();
}
function initTest(){
    var b=$('body');
    var chg=$('#changeable');
    var sub=$('#submit-btn');
    var text_input=$('#text-input');
    var html_input=$('#html-input');
    var sw=$('#exitview-switch');
    var msg_box=$('.msg-box-tem');
    initSwitchTest();
    copyText(text_input,html_input);
    text_input.unbind().on("propertychange focus input",()=>{
        copyText(text_input,html_input);
    });
    html_input.unbind().on("propertychange focus input",()=>{
        copyHtml(html_input,text_input);
    });
    sub.click((e)=>{
        log(e)
        var json=gatherBlogInfo();
        if(json){
            var re=$.post({url:'/manage/editor',async:false,data:JSON.stringify(json)}).responseJSON;
            var msg=re.message;
            showMsg(msg_box,msg);
            if(re.success)location.reload();
        }
    });


}
$(document).ready(()=>{
    initTest();
})