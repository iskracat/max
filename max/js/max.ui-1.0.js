/*
* json2
*/
var JSON;JSON||(JSON={});
(function(){function k(a){return a<10?"0"+a:a}function o(a){p.lastIndex=0;return p.test(a)?'"'+a.replace(p,function(a){var c=r[a];return typeof c==="string"?c:"\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4)})+'"':'"'+a+'"'}function l(a,j){var c,d,h,m,g=e,f,b=j[a];b&&typeof b==="object"&&typeof b.toJSON==="function"&&(b=b.toJSON(a));typeof i==="function"&&(b=i.call(j,a,b));switch(typeof b){case "string":return o(b);case "number":return isFinite(b)?String(b):"null";case "boolean":case "null":return String(b);case "object":if(!b)return"null";
e+=n;f=[];if(Object.prototype.toString.apply(b)==="[object Array]"){m=b.length;for(c=0;c<m;c+=1)f[c]=l(c,b)||"null";h=f.length===0?"[]":e?"[\n"+e+f.join(",\n"+e)+"\n"+g+"]":"["+f.join(",")+"]";e=g;return h}if(i&&typeof i==="object"){m=i.length;for(c=0;c<m;c+=1)typeof i[c]==="string"&&(d=i[c],(h=l(d,b))&&f.push(o(d)+(e?": ":":")+h))}else for(d in b)Object.prototype.hasOwnProperty.call(b,d)&&(h=l(d,b))&&f.push(o(d)+(e?": ":":")+h);h=f.length===0?"{}":e?"{\n"+e+f.join(",\n"+e)+"\n"+g+"}":"{"+f.join(",")+
"}";e=g;return h}}if(typeof Date.prototype.toJSON!=="function")Date.prototype.toJSON=function(){return isFinite(this.valueOf())?this.getUTCFullYear()+"-"+k(this.getUTCMonth()+1)+"-"+k(this.getUTCDate())+"T"+k(this.getUTCHours())+":"+k(this.getUTCMinutes())+":"+k(this.getUTCSeconds())+"Z":null},String.prototype.toJSON=Number.prototype.toJSON=Boolean.prototype.toJSON=function(){return this.valueOf()};var q=/[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,
p=/[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,e,n,r={"\u0008":"\\b","\t":"\\t","\n":"\\n","\u000c":"\\f","\r":"\\r",'"':'\\"',"\\":"\\\\"},i;if(typeof JSON.stringify!=="function")JSON.stringify=function(a,j,c){var d;n=e="";if(typeof c==="number")for(d=0;d<c;d+=1)n+=" ";else typeof c==="string"&&(n=c);if((i=j)&&typeof j!=="function"&&(typeof j!=="object"||typeof j.length!=="number"))throw Error("JSON.stringify");return l("",
{"":a})};if(typeof JSON.parse!=="function")JSON.parse=function(a,e){function c(a,d){var g,f,b=a[d];if(b&&typeof b==="object")for(g in b)Object.prototype.hasOwnProperty.call(b,g)&&(f=c(b,g),f!==void 0?b[g]=f:delete b[g]);return e.call(a,d,b)}var d,a=String(a);q.lastIndex=0;q.test(a)&&(a=a.replace(q,function(a){return"\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4)}));if(/^[\],:{}\s]*$/.test(a.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,"@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,
"]").replace(/(?:^|:|,)(?:\s*\[)+/g,"")))return d=eval("("+a+")"),typeof e==="function"?c({"":d},""):d;throw new SyntaxError("JSON.parse");}})();
/*
* jquery.iecors.js
*/
(function(b){b.ajaxSettings.xdr=function(){return window.XDomainRequest?new window.XDomainRequest:null};(function(a){b.extend(b.support,{iecors:!!a})})(b.ajaxSettings.xdr());b.support.iecors&&b.ajaxTransport(function(a){return{send:function(b,d){var c=a.xdr();c.onload=function(){d(200,"OK",{text:c.responseText},{"Content-Type":c.contentType})};if(a.xhrFields)xhr.onerror=a.xhrFields.error,xhr.ontimeout=a.xhrFields.timeout;c.open(a.type,a.url);c.send(a.hasContent&&a.data||null)},abort:function(){xdr.abort()}}})})(jQuery);
/*
* jquery.easydate.js
*/
(function(b){function e(f,b,a){!isNaN(b)&&b!=1&&(f+="s");return a.locale[f]||f}b.easydate={};b.easydate.locales={};b.easydate.locales.enUS={future_format:"%s %t",past_format:"%t %s",second:"second",seconds:"seconds",minute:"minute",minutes:"minutes",hour:"hour",hours:"hours",day:"day",days:"days",week:"week",weeks:"weeks",month:"month",months:"months",year:"year",years:"years",yesterday:"yesterday",tomorrow:"tomorrow",now:"just now",ago:"ago","in":"in"};b.easydate.locales.esCA={future_format:"%s %t",
past_format:"%s %t",second:"segon",seconds:"segons",minute:"minut",minutes:"minuts",hour:"hora",hours:"hores",day:"dia",days:"dies",week:"setmana",weeks:"setmanes",month:"mes",months:"mesos",year:"any",years:"anys",yesterday:"ahir",tomorrow:"dem\u00e0",now:"fa un moment",ago:"fa","in":"en"};var i={live:!0,set_title:!0,format_future:!0,format_past:!0,units:[{name:"now",limit:5},{name:"second",limit:60,in_seconds:1},{name:"minute",limit:3600,in_seconds:60},{name:"hour",limit:86400,in_seconds:3600},
{name:"yesterday",limit:172800,past_only:!0},{name:"tomorrow",limit:172800,future_only:!0},{name:"day",limit:604800,in_seconds:86400},{name:"week",limit:2629743,in_seconds:604800},{name:"month",limit:31556926,in_seconds:2629743},{name:"year",limit:Infinity,in_seconds:31556926}],uneasy_format:function(b){return b.toLocaleDateString()},locale:b.easydate.locales.esCA};b.easydate.format_date=function(f,h){var a=b.extend({},i,h),c=((new Date).getTime()-f.getTime())/1E3,g=Math.abs(c);if(!isNaN(c)&&!(!a.format_future&&
c<0||!a.format_past&&c>0)){for(var j in a.units){var d=a.units[j];if(!(d.past_only&&c<0||d.future_only&&c>0)&&g<d.limit){if(isNaN(d.in_seconds))return e(d.name,NaN,a);g/=d.in_seconds;g=Math.round(g);return(c<0?e("future_format",NaN,a).replace("%s",e("in",NaN,a)):e("past_format",NaN,a).replace("%s",e("ago",NaN,a))).replace("%t",g+" "+e(d.name,g,a))}}return a.uneasy_format(f)}}})(jQuery);
/*
* hogan.js
*/
var HoganTemplate=function(){function n(a){this.text=a}n.prototype={r:function(){return""},v:function(a){a=String(a===null?"":a);return s.test(a)?a.replace(u,"&amp;").replace(v,"&lt;").replace(w,"&gt;").replace(l,"&#39;").replace(j,"&quot;"):a},render:function(a,c,f){return this.r(a,c,f)},rp:function(a,c,f,e){a=f[a];return!a?"":a.r(c,f,e)},rs:function(a,c,f){var e="",g=a[a.length-1];if(!p(g))return f(a,c);for(var b=0;b<g.length;b++)a.push(g[b]),e+=f(a,c),a.pop();return e},s:function(a,c,f,e,g,b,i){if(p(a)&&
a.length===0)return!1;!e&&typeof a=="function"&&(a=this.ls(a,c,f,g,b,i));f=a===""||!!a;!e&&f&&c&&c.push(typeof a=="object"?a:c[c.length-1]);return f},d:function(a,c,f,e){var g=a.split("."),b=this.f(g[0],c,f,e),i=null;if(a==="."&&p(c[c.length-2]))return c[c.length-1];for(a=1;a<g.length;a++)b&&typeof b=="object"&&g[a]in b?(i=b,b=b[g[a]]):b="";if(e&&!b)return!1;!e&&typeof b=="function"&&(c.push(i),b=this.lv(b,c,f),c.pop());return b},f:function(a,c,f,e){for(var g=!1,b=null,i=!1,m=c.length-1;m>=0;m--)if((b=
c[m])&&typeof b=="object"&&a in b){g=b[a];i=!0;break}if(!i)return e?!1:"";!e&&typeof g=="function"&&(g=this.lv(g,c,f));return g},ho:function(a,c,f,e,g){a=a.call(c,e,function(b){return Hogan.compile(b,{delimiters:g}).render(c,f)});this.b=Hogan.compile(a.toString(),{delimiters:g}).render(c,f);return!1},b:"",ls:function(a,c,f,e,g,b){var c=c[c.length-1],i=a.call(c);return a.length>0?this.ho(a,c,f,this.text.substring(e,g),b):typeof i=="function"?this.ho(i,c,f,this.text.substring(e,g),b):i},lv:function(a,
c,f){c=c[c.length-1];return Hogan.compile(a.call(c).toString()).render(c,f)}};var u=/&/g,v=/</g,w=/>/g,l=/\'/g,j=/\"/g,s=/[&<>\"\']/,p=Array.isArray||function(a){return Object.prototype.toString.call(a)==="[object Array]"};return n}(),Hogan=function(){function n(b,a){function m(){o.length>0&&(k.push(new String(o)),o="")}function c(b,a){m();var d;if(d=b)a:{d=!0;for(var i=n;i<k.length;i++)if(d=k[i].tag&&g[k[i].tag]<g._v||!k[i].tag&&k[i].match(p)===null,!d){d=!1;break a}}if(d){d=n;for(var f;d<k.length;d++)if(!k[d].tag){if((f=
k[d+1])&&f.tag==">")f.indent=k[d].toString();k.splice(d,1)}}else a||k.push({tag:"\n"});j=!1;n=k.length}function d(b,a){var d="="+q,m=b.indexOf(d,a),c=u(b.substring(b.indexOf("=",a)+1,m)).split(" ");r=c[0];q=c[1];return m+d.length-1}var f=b.length,e=0,t=null,l=null,o="",k=[],j=!1,h=0,n=0,r="{{",q="}}";a&&(a=a.split(" "),r=a[0],q=a[1]);for(h=0;h<f;h++)e==0?v(r,b,h)?(--h,m(),e=1):b.charAt(h)=="\n"?c(j):o+=b.charAt(h):e==1?(h+=r.length-1,t=(l=g[b.charAt(h+1)])?b.charAt(h+1):"_v",t=="="?(h=d(b,h),e=0):
(l&&h++,e=2),j=h):v(q,b,h)?(k.push({tag:t,n:u(o),otag:r,ctag:q,i:t=="/"?j-q.length:h+r.length}),o="",h+=q.length-1,e=0,t=="{"&&h++):o+=b.charAt(h);c(j,!0);return k}function u(b){return b.trim?b.trim():b.replace(/^\s*|\s*$/g,"")}function v(b,a,m){if(a.charAt(m)!=b.charAt(0))return!1;for(var c=1,d=b.length;c<d;c++)if(a.charAt(m+c)!=b.charAt(c))return!1;return!0}function w(b,a,c,f){for(var a=[],d=null,e=null;b.length>0;){e=b.shift();if(!(d=e.tag=="#"))if(!(d=e.tag=="^"))a:{for(var d=e,g=f,j=0,l=g.length;j<
l;j++)if(g[j].o==d.n){d.tag="#";d=!0;break a}d=void 0}if(d)c.push(e),e.nodes=w(b,e.tag,c,f),a.push(e);else if(e.tag=="/"){if(c.length===0)throw Error("Closing tag without opener: /"+e.n);d=c.pop();if(b=e.n!=d.n){var o;a:{b=0;for(c=f.length;b<c;b++)if(f[b].c==e.n&&f[b].o==d.n){o=!0;break a}}b=!o}if(b)throw Error("Nesting error: "+d.n+" vs. "+e.n);d.end=e.i;return a}else a.push(e)}if(c.length>0)throw Error("missing closing tag: "+c.pop().n);return a}function l(b){return b.replace(e,"\\\\").replace(a,
'\\"').replace(c,"\\n").replace(f,"\\r")}function j(b){return~b.indexOf(".")?"d":"f"}function s(b){for(var a="",c=0,e=b.length;c<e;c++){var d=b[c].tag;if(d=="#"){var d=b[c].nodes,f=j(b[c].n),g=b[c].i,n=b[c].end,p=b[c].otag+" "+b[c].ctag,d="if(_.s(_."+f+'("'+l(b[c].n)+'",c,p,1),c,p,0,'+g+","+n+', "'+p+'")){b += _.rs(c,p,function(c,p){ var b = "";'+s(d)+'return b;});c.pop();}else{b += _.b; _.b = ""};';a+=d}else d=="^"?(d=b[c].nodes,d="if (!_.s(_."+j(b[c].n)+'("'+l(b[c].n)+'",c,p,1),c,p,1,0,0,"")){'+
s(d)+"};",a+=d):d=="<"||d==">"?a+='b += _.rp("'+l(b[c].n)+'",c[c.length - 1],p,"'+(b[c].indent||"")+'");':d=="{"||d=="&"?(d="b += (_."+j(b[c].n)+'("'+l(b[c].n)+'",c,p,0));',a+=d):d=="\n"?a+='b += "\\n"'+(b.length-1==c?"":" + i")+";":d=="_v"?(d="b += (_.v(_."+j(b[c].n)+'("'+l(b[c].n)+'",c,p,0)));',a+=d):d===void 0&&(d='"'+l(b[c])+'"',a+="b += "+d+";")}return a}var p=/\S/,a=/\"/g,c=/\n/g,f=/\r/g,e=/\\/g,g={"#":1,"^":2,"/":3,"!":4,">":5,"<":6,"=":7,_v:8,"{":9,"&":10};return{scan:n,parse:function(b,a){a=
a||{};return w(b,"",[],a.sectionTags||[])},cache:{},compile:function(b,a){var a=a||{},c=this.cache[b];if(c)return c;var e=this.parse(n(b,a.delimiters),a),c=a,e='i = i || "";var c = [cx];var b = i + "";var _ = this;'+s(e)+"return b;";c.asString?c="function(cx,p,i){"+e+";}":(c=new HoganTemplate(b),c.r=new Function("cx","p","i",e));return this.cache[b]=c}}}();
if(typeof module!=="undefined"&&module.exports)module.exports=Hogan,module.exports.Template=HoganTemplate;else if(typeof define==="function"&&define.amd)define(function(){return Hogan});else if(typeof exports!=="undefined")exports.Hogan=Hogan,exports.HoganTemplate=HoganTemplate;
/*
* max.templates.js
*/
var MSTCH_MAXUI_MAIN_UI='<div id="maxui-container">{{#username}} <div id="maxui-mainpanel">   <div id="maxui-newactivity">      <div class="maxui-avatar">           <img src="{{avatar}}">      </div>      <div class="textbox">           <textarea>{{literals.new_activity_text}}</textarea>           <input type="button" class="send" value="{{literals.new_activity_post}}">      </div>   </div>   <div id="maxui-search-filters">   </div>   <div id="maxui-timeline">      <div class="wrapper">          <div id="maxui-activities">          </div>      </div>   </div>   <div id="maxui-more-activities">        <input type="button" class="load" value="{{literals.load_more}}">   </div>  </div> </div>{{/username}}{{^username}}  No s\'ha definit cap usuari{{/username}}</div>',
MSTCH_MAXUI_ACTIVITIES='{{#activities}}<div class="maxui-activity" id="{{id}}" userid="{{actor.id}}" username="{{actor.username}}">    <div class="maxui-avatar">        <img src="{{#avatarURL}}{{actor.username}}{{/avatarURL}}">    </div>    <div class="maxui-activity-content">        <div>          <span class="maxui-displayname">{{actor.displayName}}</span>          <span class="maxui-username">{{actor.username}}</span>        </div>        <div>            <p class="maxui-body">{{#formattedText}}{{object.content}}{{/formattedText}}</p>        </div>        <div class="maxui-publisheddate">{{#formattedDate}}{{published}}{{/formattedDate}}</div>    </div>    <div class="maxui-footer">        <div class="maxui-actions">            <ul>                <li><span class="maxui-commentaction">{{literals.toggle_comments}}  {{#replies}}({{replies.totalItems}}){{/replies}}</span></li>            </ul>        </div>    </div>    <div class="maxui-comments" style="display: none">        <div class="maxui-commentsbox">            {{#replies.items}}            <div class="maxui-comment" id="{{id}}" userid="{{author.id}}" displayname="{{author.username}}">                <div class="maxui-avatar">                    <img src="{{#avatarURL}}{{author.username}}{{/avatarURL}}">                </div>                <div class="maxui-activity-content">                    <div>                      <span class="maxui-displayname">{{author.username}}</span>                      <span class="maxui-username">{{author.displayName}}</span>                    </div>                    <div>                        <p class="maxui-body">{{content}}</p>                    </div>                    <div class="maxui-publisheddate">{{#formattedDate}}{{published}}{{/formattedDate}}</div>                </div>            </div>            {{/replies.items}}        </div>        <div class="maxui-newcommentbox">            <div class="maxui-newcommentBoxContainer">                <textarea class="maxui-commentBox"></textarea>            </div>            <div class="maxui-newcommentbutton">                <input type="button" class="send" value="{{literals.new_comment_post}}"/>            </div>        </div>    </div>    <div class="maxui-clear"></div></div>{{/activities}}',
MSTCH_MAXUI_COMMENTS='{{#comments}}<div class="maxui-comment" id="{{id}}" userid="{{author.id}}" displayname="{{author.username}}">    <div class="maxui-avatar">        <img src="{{#avatarURL}}{{author.username}}{{/avatarURL}}">    </div>    <div class="maxui-activity-content">        <div>          <span class="maxui-displayname">{{author.username}}</span>          <span class="maxui-username">{{author.displayName}}</span>        </div>        <div>            <p class="maxui-body">{{content}}</p>        </div>        <div class="maxui-publisheddate">{{#formattedDate}}{{published}}{{/formattedDate}}</div>    </div></div>{{/comments}}',
MSTCH_MAXUI_FILTERS='{{#filters}}<div class="maxui-filter" type="{{type}}" value="{{value}}"><span>{{value}}<a class="close" href="">X</a></span></div>{{/filters}}',MAXUI_MAIN_UI=Hogan.compile(MSTCH_MAXUI_MAIN_UI),MAXUI_ACTIVITIES=Hogan.compile(MSTCH_MAXUI_ACTIVITIES),MAXUI_COMMENTS=Hogan.compile(MSTCH_MAXUI_COMMENTS),MAXUI_FILTERS=Hogan.compile(MSTCH_MAXUI_FILTERS);
/*
* max.client.js
*/
if(!Object.keys)Object.keys=function(a){var b=[],c;for(c in a)Object.prototype.hasOwnProperty.call(a,c)&&b.push(c);return b};String.prototype.format=function(){var a=arguments;return this.replace(/\{\d+\}/g,function(b){return a[b.match(/\d+/)]})};
function MaxClient(a){this.url=a;this.mode="jquery";this.ROUTES={users:"/people",user:"/people/{0}",avatar:"/people/{0}/avatar",user_activities:"/people/{0}/activities",timeline:"/people/{0}/timeline",user_comments:"/people/{0}/comments",user_shares:"/people/{0}/shares",user_likes:"/people/{0}/likes",follows:"/people/{0}/follows",follow:"/people/{0}/follows/{1}",subscriptions:"/people/{0}/subscriptions",activities:"/activities",activity:"/activities/{0}",comments:"/activities/{0}/comments",comment:"/activities/{0}/comments/{1}",
likes:"/activities/{0}/likes",like:"/activities/{0}/likes/{1}",shares:"/activities/{0}/shares",share:"/activities/{0}/shares/{1}"}}MaxClient.prototype.setMode=function(a){this.mode=a};MaxClient.prototype.setActor=function(a){this.actor={objectType:"person",username:a}};
MaxClient.prototype.POST=function(a,b,c){resource_uri="{0}{1}".format(this.url,a);this.mode=="jquery"?jQuery.ajax({url:resource_uri,beforeSend:function(a){a.setRequestHeader("X-Oauth-Token",_MAXUI.settings.oAuthToken);a.setRequestHeader("X-Oauth-Username",_MAXUI.settings.username);a.setRequestHeader("X-Oauth-Scope","widgetcli")},type:"POST",data:JSON.stringify(b),async:!0,dataType:"json"}).always(function(a,b,e){e.status==200|e.status==201&&c.call(a)}):(a={},a[gadgets.io.RequestParameters.CONTENT_TYPE]=
gadgets.io.ContentType.JSON,a[gadgets.io.RequestParameters.METHOD]=gadgets.io.MethodType.POST,a[gadgets.io.RequestParameters.REFRESH_INTERVAL]=1,a[gadgets.io.RequestParameters.POST_DATA]=JSON.stringify(b),a[gadgets.io.RequestParameters.HEADERS]={"X-Oauth-Token":_MAXUI.settings.oAuthToken,"X-Oauth-Username":_MAXUI.settings.username,"X-Oauth-Scope":"widgetcli"},console.log(a),gadgets.io.makeRequest(resource_uri,function(a){c.call(a.data)},a));return!0};
MaxClient.prototype.GET=function(a,b,c){resource_uri="{0}{1}".format(this.url,a);Object.keys(b).length>0&&(resource_uri+="?"+jQuery.param(b,!0));this.mode=="jquery"?jQuery.ajax({url:resource_uri,beforeSend:function(a){a.setRequestHeader("X-Oauth-Token",_MAXUI.settings.oAuthToken);a.setRequestHeader("X-Oauth-Username",_MAXUI.settings.username);a.setRequestHeader("X-Oauth-Scope","widgetcli")},type:"GET",async:!0,dataType:"json"}).always(function(a,b,e){e.status==200|e.status==201&&c.call(a)}):(a={},
a[gadgets.io.RequestParameters.CONTENT_TYPE]=gadgets.io.ContentType.JSON,a[gadgets.io.RequestParameters.METHOD]=gadgets.io.MethodType.GET,a[gadgets.io.RequestParameters.REFRESH_INTERVAL]=1,a[gadgets.io.RequestParameters.HEADERS]={"X-Oauth-Token":_MAXUI.settings.oAuthToken,"X-Oauth-Username":_MAXUI.settings.username,"X-Oauth-Scope":"widgetcli"},gadgets.io.makeRequest(resource_uri,function(a){console.log(data);c.call(a.data)},a));return!0};
MaxClient.prototype.getUserTimeline=function(a,b){var c=this.ROUTES.timeline.format(a);query=arguments.length>2?arguments[3]:{};this.GET(c,query,b)};MaxClient.prototype.getActivities=function(a,b,c){var d=this.ROUTES.activities;query=arguments.length>3?arguments[3]:{};if(b.length>0)query.contexts=b;this.GET(d,query,c)};MaxClient.prototype.getCommentsForActivity=function(a,b){route=this.ROUTES.comments.format(a);this.GET(route,{},b)};
MaxClient.prototype.addComment=function(a,b,c){var d={actor:{},object:{objectType:"comment",content:""}};d.actor=this.actor;d.object.content=a;route=this.ROUTES.comments.format(b);this.POST(route,d,c)};MaxClient.prototype.addActivity=function(a,b,c){query={object:{objectType:"note",content:""}};if(b.length>0)query.contexts=b;query.object.content=a;route=this.ROUTES.user_activities.format(this.actor.username);this.POST(route,query,c)};
MaxClient.prototype.follow=function(a){query={object:{objectType:"person",username:""}};query.object.username=a;route=this.ROUTES.follow.format(this.actor.username,a);resp=this.POST(route,query)};
/*
* max.ui.js
*/
(function(b){b.fn.maxUI=function(a){var d=this;if(!window._MAXUI)window._MAXUI={};var c=b.extend({new_activity_text:"Write something",new_activity_post:"Post activity",toggle_comments:"Comments",new_comment_post:"Post comment",load_more:"Load more"},a.literals);delete a.literals;_MAXUI.settings=b.extend({maxRequestsAPI:"jquery",maxServerURL:"http://max.beta.upcnet.es",contextFilter:[],activitySource:"timeline",literals:c},a);for(key in _MAXUI.settings.literals)value=_MAXUI.settings.literals[key],
_MAXUI.settings.literals[key]=d.utf8_decode(value);if(!this.isCORSCapable()&&_MAXUI.settings.maxServerURLAlias)_MAXUI.settings.maxServerURL=_MAXUI.settings.maxServerURLAlias;_MAXUI.settings.avatarURLpattern||(_MAXUI.settings.avatarURLpattern=_MAXUI.settings.maxServerURL+"/people/{0}/avatar");this.maxClient=new MaxClient(_MAXUI.settings.maxServerURL);this.maxClient.setMode(_MAXUI.settings.maxRequestsAPI);this.maxClient.setActor(_MAXUI.settings.username);a=b.extend(_MAXUI.settings,{avatar:_MAXUI.settings.avatarURLpattern.format(_MAXUI.settings.username)});
this.html(MAXUI_MAIN_UI.render(a));this.printActivities();b("#maxui-newactivity .send").click(function(){d.sendActivity()});b("#maxui-more-activities .load").click(function(){d.loadMoreActivities()});b("#maxui-activities").on("click",".maxui-commentaction",function(){b(this).closest(".maxui-activity").find(".maxui-comments").toggle()});b("#maxui-activities").on("click",".maxui-hashtag",function(){event.preventDefault();d.addFilter({type:"hashtag",value:this.text})});b("#maxui-search-filters").on("click",
".close",function(){event.preventDefault();var a=$(this.parentNode.parentNode);d.delFilter({type:a.attr("type"),value:a.attr("value")})});b("#maxui-activities").on("click",".maxui-comments .send",function(a){a.preventDefault();var a=b(this).closest(".maxui-comments").find("textarea").val(),c=b(this).closest(".maxui-activity").attr("id");d.maxClient.addComment(a,c,function(){b("#activityContainer textarea").val("");d.printCommentsForActivity(this.object.inReplyTo[0].id)})});b("#maxui-newactivity textarea").focusin(function(){b(this).val()==
_MAXUI.settings.literals.new_activity_text&&(b(this).val(""),b(this).attr("class",""))});b("#maxui-newactivity textarea").focusout(function(){b(this).val()==""?(b(this).val(_MAXUI.settings.literals.new_activity_text),b(this).attr("class","empty")):b(this).attr("class","")});return d};b.fn.reloadFilters=function(){params={filters:window._MAXUI.filters};var a=MAXUI_FILTERS.render(params);b("#maxui-search-filters").html(a)};b.fn.delFilter=function(a){var b=!1,c=-1;for(i=0;i<window._MAXUI.filters.length;i++)window._MAXUI.filters[i].value==
a.value&window._MAXUI.filters[i].type==a.type&&(c=i,b=!0);b&&delete window._MAXUI.filters[c];this.reloadFilters()};b.fn.addFilter=function(a){if(!window._MAXUI.filters)window._MAXUI.filters=[];var b=!1;for(i=0;i<window._MAXUI.filters.length;i++)window._MAXUI.filters[i].value==a.value&window._MAXUI.filters[i].type==a.type&&(b=!0);b||(window._MAXUI.filters.push(a),this.reloadFilters())};b.fn.isCORSCapable=function(){return(new XMLHttpRequest).withCredentials!=void 0?!0:!1};b.fn.Settings=function(){return maxui.settings};
b.fn.sendActivity=function(){maxui=this;this.maxClient.addActivity(b("#maxui-newactivity textarea").val(),_MAXUI.settings.contextFilter,function(){b("#maxui-newactivity textarea").val("");var a=b(".maxui-activity:first");a.length>0?(filter={after:a.attr("id")},maxui.printActivities(filter)):maxui.printActivities()})};b.fn.loadMoreActivities=function(){maxui=this;filter={before:b(".maxui-activity:last").attr("id")};maxui.printActivities(filter)};b.fn.formatDate=function(a){var d=new Date;if(a=a.match("^([-+]?)(\\d{4,})(?:-?(\\d{2})(?:-?(\\d{2})(?:[Tt ](\\d{2})(?::?(\\d{2})(?::?(\\d{2})(?:\\.(\\d{1,3})(?:\\d+)?)?)?)?(?:[Zz]|(?:([-+])(\\d{2})(?::?(\\d{2}))?)?)?)?)?)?$")){for(var c=
[2,3,4,5,6,7,8,10,11],e=c.length-1;e>=0;--e)a[c[e]]=typeof a[c[e]]!="undefined"&&a[c[e]].length>0?parseInt(a[c[e]],10):0;a[1]=="-"&&(a[2]*=-1);c=Date.UTC(a[2],a[3]-1,a[4],a[5],a[6],a[7],a[8]);typeof a[9]!="undefined"&&a[9].length>0&&(c+=(a[9]=="+"?-1:1)*(a[10]*36E5+a[11]*6E4));a[2]>=0&&a[2]<=99&&(c-=59958144E6);d.setTime(c);return formatted=b.easydate.format_date(d)}else return null};b.fn.utf8_decode=function(a){var b=[],c=0,e=0,f=0,g=0,h=0;for(a+="";c<a.length;)f=a.charCodeAt(c),f<128?(b[e++]=String.fromCharCode(f),
c++):f>191&&f<224?(g=a.charCodeAt(c+1),b[e++]=String.fromCharCode((f&31)<<6|g&63),c+=2):(g=a.charCodeAt(c+1),h=a.charCodeAt(c+2),b[e++]=String.fromCharCode((f&15)<<12|(g&63)<<6|h&63),c+=3);return b.join("")};b.fn.formatActivity=function(a,d){maxui=this;var c=MAXUI_ACTIVITIES.render({literals:_MAXUI.settings.literals,activities:a,formattedDate:function(){return function(a){a=this.published;return maxui.formatDate(a)}},formattedText:function(){return function(a){a=this.object.content;return maxui.formatText(a)}},
avatarURL:function(){return function(){var a=this.hasOwnProperty("actor")?this.actor.username:this.author.username;return _MAXUI.settings.avatarURLpattern.format(a)}}});d=="beggining"?b("#maxui-activities").prepend(c):b("#maxui-activities").append(c)};b.fn.formatComment=function(a,d){maxui=this;var c=MAXUI_COMMENTS.render({literals:_MAXUI.settings.literals,comments:a,formattedDate:function(){return function(a){a=this.published;return maxui.formatDate(a)}},formattedText:function(){return function(a){a=
this.object.content;return maxui.formatText(a)}},avatarURL:function(){return function(){var a=this.hasOwnProperty("actor")?this.actor.username:this.author.username;return _MAXUI.settings.avatarURLpattern.format(a)}}});b(".maxui-activity#"+d+" .maxui-commentsbox").html(c)};b.fn.formatText=function(a){a&&(a=a.replace(/((https?\:\/\/)|(www\.))(\S+)(\w{2,4})(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/gi,function(a){var b=a;b.match("^https?://")||(b="http://"+b);return'<a href="'+b+'">'+a+"</a>"}),a=a.replace(/(\s|^)#{1}(\w+)/gi,
function(a){return'<a class="maxui-hashtag" href="{0}/{}">'+a+"</a>"}));return a};b.fn.printActivities=function(){var a=this,b=[],c="beggining";arguments.length>0&&arguments[0].before&&(c="end");if(_MAXUI.settings.activitySource=="timeline"){var e=this.maxClient.getUserTimeline;b.push(_MAXUI.settings.username);b.push(function(){a.formatActivity(this.items,c)})}else if(_MAXUI.settings.activitySource=="activities")e=this.maxClient.getActivities,b.push(_MAXUI.settings.username),b.push(_MAXUI.settings.contextFilter),
b.push(function(){a.formatActivity(this.items,c)});arguments.length>0&&b.push(arguments[0]);e.apply(this.maxClient,b)};b.fn.printCommentsForActivity=function(a){var b=this,c=[];c.push(a);c.push(function(){b.formatComment(this.items,a)});this.maxClient.getCommentsForActivity.apply(this.maxClient,c)}})(jQuery);
/*
* max.loader.js
*/
window.setTimeout(function () {
    if(window._MAXUI.onReady && !window._MAXUI.hasRun){
        window._MAXUI.hasRun = true;
        _MAXUI.onReady();
    }
  },0)