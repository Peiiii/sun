function log(text){console.log(text);}
function initMarked(){
  var myMarked = marked;
  myMarked.setOptions({
  renderer: new myMarked.Renderer(),
  highlight: function(code) {
    return hljs.highlightAuto(code).value;
  },
  pedantic: false,
  gfm: true,
  tables: true,
  breaks: true,
  sanitize: true,
  smartLists: true,
  smartypants: true,
  xhtml: false
    });
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
    var format=head.format;
    if(format=='md'||format=='markdown')return;
    var html=src.html();
    tar.val(html);
}
function renderText(text){
    var head;var body;
    [head,body]=getHeadAndBody(text);
    if(!head)return text;
    var dic=head.strip('/*').strip('*/').toDict(';');
    if(!dic.hasOwnProperty('format'))dic.format='text/plain';
    var format=dic.format;
    if(format=='markdown' || format=='md')return marked(body);
    return body;
}

function getHead(text){
    var head;var body;
    [head,body]=getHeadAndBody(text);
    if(!head)return {};
    var dic=head.strip('/*').strip('*/').toDict(';');log(dic);
    if(!dic.hasOwnProperty('format'))dic.format='text/plain';
    return dic;
}
function copyText(src,tar){
    var text=src.val();
    text=renderText(text);
    tar.html(text);
}
//---------Class Editor----------------//
class Editor{
    constructor(selector){
        var el=$(selector);
        this.selector=selector;
        this.el=el;
        this.keys_input_area=el.find('#info-bar');
        this.key_inputs=el.find('.key-input');
        this.msg_box=$('.msg-box-tem');
        this.mode='create';this.submit_url='/manage/editor';
        this.default_values={
            category:'demo',author:'WP'
        };
        this.no_empty_list=['title','category','tags','format_used'];
        this.keys=['title','category','tags','format_used','keywords','description',
                    'digest','author','visible','mood','status','text','html','md'];

    }
    fillInput(key,value){
        var input=this.input(key);
        if( ['input','textarea','select'].indexOf(input[0].tagName.toLowerCase())>-1){input.val(value);return}
        else input.html(value);
    }
    editBlog(blog,mode='alter'){
        this.mode=mode;
        log(blog)
        for(var i=0;i<this.keys.length;i++){
            this.fillInput(this.keys[i],blog[this.keys[i]]);
        }
        this.fillDefault();
        this.display();
    }
    input(key){
        return this.getKeyInputArea(key);
    }
    getKeyInputArea(key){
        for(var i=0;i<this.key_inputs.length;i++){
            if($(this.key_inputs[i]).attr('key')==key) return $(this.key_inputs[i]);
        }
    }
    fillIfEmpty(key,value){
        var input=this.input(key);
        if(input.val().trim()=='')input.val(value);
    }
    fillDefault(){
         this.fillIfEmpty('category',this.default_values.category);
         this.fillIfEmpty('author',this.default_values.author);
    }
    display(){
        location.href=this.selector;
    }
    submit(){
        this.fillDefault();
        var json=this.prepareInfo();
        if(json){
            if(this.mode=='alter'){json.opr_type='alter';json.id=this.blog_id;}
            else {json.opr_type='create';json.id=null;}
            var re=$.post({url:this.submit_url,async:false,data:JSON.stringify(json)}).responseJSON;
            var msg=re.message;
            this.showMsg(msg);
            if(re.success){
                var msg=`保存成功，<a href="/manage#editor">刷新本页？</a>或者${re}`
                showMsg(msg_box,)
            };
        }
    }
    showMsg(msg){
        showMsg(this.msg_box,msg);
    }
    prepareInfo(){

        var json={};
        for(var i=0;i<this.key_inputs.length;i++){
            var input=$(this.key_inputs[i]);
            var key=input.attr('key');
            var value;
            if(input.hasClass('html-input'))value=input.html();
            else value=input.val().trim();
            if(this.no_empty_list.indexOf(key)>-1){
                if(value ==''){ this.showMsg(key+' can not  be empty.');return false;}
            }
            json[key]=value;
        }
        json.tags=json.tags.split(';');
        if(json.format_used=='plain-text'){null}
        else if(json.format_used=='markdown')json.md=json.text;
        else if(json.format_used=='html')json.html=json.text;
        return json;
    }

}

//--------------------- Functions below are somewhat useless--------------------------//
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
        var sw_dv=switches.doubleview[0];
        sw_dv.easyTurnOff();
    });
    switches['editable']=[];
    switches.editable.push(sw);
}
//-----------------insert blog and edit-----------//

//----------------cmd---------------//

function initCommandButton(){
    var btn=$('.cmd-btn');
    var input=$('.cmd-input');
    var msg_box=$('.msg-box-tem');
    var funcs={
        "edit":()=>{
            var sw=switches.editable[0];
            var btn=$('#btn-editable');
            show(btn);
            sw.easyTurnOn();
            return true;
        },
        "exit":()=>{
            var sw=switches.editable[0];
            sw.easyTurnOff();
            return true;
        },
        "mode":(param)=>{
            if(param=='close'){
                fman.closeMode();
                return true;
            }
            else if(param=='dark'){
                fman.setMode('mode-dark');
            return true;
            }
            return false;
        },
        "#":(param)=>{
            location.href="#" + param;
        }
    }
    new Commander(input,btn,funcs,msg_box);
}
//--------------gather blog info-----------------//

//----------end cmd-----------//
function initSwitchTest(){
    initEditableSwitch();
    initCommandButton();
    initSwitch();
}
function initEditor(){
    var editor_app=new Editor('#editor');
    var fman=new FaceManager('#editor');
    var editor=$('#editor');
    var app=editor_app;
    var b=$('body');
    var chg=$('#changeable');
    var sub=$('#submit-btn');
    var btn_save=editor.find('.btn-save');
    var text_input=$('#text-input');
    var html_input=$('#html-input');
    var sw=$('#exitview-switch');
    var msg_box=$('.msg-box-tem');
    initSwitchTest();
    initMarked();
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
    btn_save.click((e)=>{
        editor_app.submit();
    });
    text_input.keydown((e)=>{
        if(e.keyCode==9){
            if (e.preventDefault) {
                e.preventDefault();
            }
            else {
                window.event.returnValue = false;
            }
            text_input.val(text_input.val()+'    ');
        }
    })

}
$(document).ready(()=>{
    initEditor();
})