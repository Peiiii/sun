
class WordQuerier{
    constructor(base_url='http://www.iciba.com'){
        this.base_url=base_url;
    }
    get(url){}
    joinPath(latter){return this.base_url+'/'+latter;}
    query(word){
        var url=this.joinPath(word);
        var re=$.post({url:'/proxy/get',data:JSON.stringify({url:url}),async:false});
        return this.parse(re.responseText);
    }
    parse(html){
       var doc=$(html);
       var s1=doc.find('.container-left').find('.js-base-info').find('.in-base');
       var item1=s1.find('.in-base-top').html()
       var item2=s1.find('.base-list').html()
       var item3=s1.find('.change').html();
       var html='';
       if(item1)html+=item1;
       if(item2)html+=item2;
       if(item3)html+=item3;
       return html;
    }
}
flag('query opend');
querier=new WordQuerier();
$(document).ready(()=>{
    var blogs=$('.blog');
    var msg_box=$('.msg-box');
    blogs.map((n,b)=>{
        b=$(b);
        b.click(()=>{
            var text=window.getSelection().toString();
            if(text.trim()=='')return hideMsg(msg_box);
            slog(text);
            var text=querier.query(text);
            showMsg(msg_box,text);
        })
    })

})



(function($){
    $.fn.extend({
        "selectText":function(value){
            value=$.extend({
                "delays":300
                },value);

            var $this = $(this);

            //鼠标抬起进，获取选择文字的字数。并根据字数，是否显示弹出层
            $this.mouseup(function(event){

                //IE和火狐兼容性的处理函数。
                function selectText(){
                    if(document.selection){
                        return document.selection.createRange().text;// IE
                    }else{
                        return  window.getSelection().toString(); //标准
                    }
                }

                var str = selectText();

                var l = event.clientX;
                var t = event.clientY;

                if(str.length > 0){
                    $this.next("div").html(str).css({"top":t+10,"left":l+10}).delay(value.delays).fadeIn();
                }
            });

            //点击文档任何位置，让显示的层消失
            $(document).click(function(){
                $this.next("div").fadeOut();
            })

            //阻止冒泡，防止第一次选中文字时，由于冒泡，而触发了$(document).click事件
            $this.click(function(event){
                event.stopPropagation();
            });

            return $this;
        }
    })
})(jQuery)