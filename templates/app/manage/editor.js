function log(text){console.log(text);}
editor_config={

}
class FaceManager{
    constructor(selector){
        this.selector=selector;
        this.el=$(selector);
        this.mode='none';
    }
    setMode(mode){
        this.mode=mode;
        this.executeMode();
    }
    closeMode(){
        this.el.removeClass('mode-dark');
    }
    executeMode(){
        this.el.addClass(this.mode);
    }
}
function copyHtml(src,tar){
    var head=getHead(tar.val());
    if(head=='md'||head=='markdown')return;
    var html=src.html();
    tar.val(html);
}
function renderText(text){
    var text2=text.split('\n');
    var head=text2[0].trim().toLowerCase();
    var body=text2.slice(1,text.length).join('\n');
    if(head[0]!='@')return text;
    head=head.slice(1,head.length);
    if(head=='markdown' || head=='md')return marked(body);
    return text;
}
function getHead(text){
    var text2=text.split('\n');
    var head=text2[0].trim().toLowerCase();
    if(head[0]!='@')return null;
    head=head.slice(1,head.length);
    return head;
}
function copyText(src,tar){
    var text=src.val();
    text=renderText(text);
    tar.html(text);
}
class Editor{
    constructor(selector){
        var el=$(selector);
        this.selector=selector;
        this.el=el;
        this.text_input=el.find('#text-input');
        this.html_input=el.find('#html-input');
        this.title_input=el.find('#title-input');
        this.cate_input=el.find('#cate-input');
        this.tags_input=el.find('#tags-input');
        this.msg_box=$('.msg-box-tem');
        this.mode='create';this.submit_url='/manage/editor';
    }
    editBlog(blog,mode='alter'){
        this.mode=mode;
        this.text_input.val(blog.text);
        this.html_input.html(blog.html);
        this.title_input.val(blog.title);
        this.cate_input.val(blog.category);
        this.tags_input.val(blog.tags.join(';'));
        this.blog_id=blog.id;
        this.display();
    }
    display(){
        location.href=this.selector;
    }
    submit(){
        var json=this.prepareInfo();
        if(json){
            if(this.mode=='alter'){json.opr_type='alter';json.id=this.blog_id;}
            else {json.opr_type='create';json.id=null;}
            var re=$.post({url:this.submit_url,async:false,data:JSON.stringify(json)}).responseJSON;
            var msg=re.message;
            showMsg(this.msg_box,msg);
            if(re.success)location.reload();
        }
    }
    prepareInfo(){
        var title=this.title_input.val();
        var cate=this.cate_input.val();
        var tags=this.tags_input.val().split(';');
        var md=this.text_input.val();
        if(title.trim()==''){showMsg(this.msg_box,'标题不能为空！');return false;}
        if(cate.trim()==''){showMsg(this.msg_box,'目录不能为空！');return false;}
        if(md.trim()==''){showMsg(this.msg_box,'文章不能为空');return false;}
        var json={title:title,category:cate,tags:tags,md:md};
        return json;
    }

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
//-----------------insert blog and edit-----------//

//----------------cmd---------------//
function checkCmd(text){
    text=text.toLowerCase();
    return text;
}
function executeCmd(cmd){
    var sw=switches.editable[0];
    var btn=$('#btn-editable');
    switch(cmd){
        case ":edit":
            show(btn);
            sw.easyTurnOn();
            return true;
        case ":exit":
            sw.easyTurnOff();
            return true;
        case ":mode dark":
            fman.setMode('mode-dark');
            return true;
        case ":mode close":
            fman.closeMode();
            return true;
        case "#editor":
            location.href='#editor';
            return true;
        case "#alter":
            location.href="#alter";
            return true;
        default:
            return false;
    }
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

//----------end cmd-----------//
function initSwitchTest(){
    initEditableSwitch();
    initCommandButton();
    initSwitch();
}
function initEditor(){
    editor_app=new Editor('#editor');
    fman=new FaceManager('#editor');
    var app=editor_app;
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
        editor_app.submit();
    });


}
$(document).ready(()=>{
    initEditor();
})