(function(t){function e(e){for(var n,i,c=e[0],o=e[1],l=e[2],_=0,d=[];_<c.length;_++)i=c[_],Object.prototype.hasOwnProperty.call(a,i)&&a[i]&&d.push(a[i][0]),a[i]=0;for(n in o)Object.prototype.hasOwnProperty.call(o,n)&&(t[n]=o[n]);u&&u(e);while(d.length)d.shift()();return r.push.apply(r,l||[]),s()}function s(){for(var t,e=0;e<r.length;e++){for(var s=r[e],n=!0,c=1;c<s.length;c++){var o=s[c];0!==a[o]&&(n=!1)}n&&(r.splice(e--,1),t=i(i.s=s[0]))}return t}var n={},a={app:0},r=[];function i(e){if(n[e])return n[e].exports;var s=n[e]={i:e,l:!1,exports:{}};return t[e].call(s.exports,s,s.exports,i),s.l=!0,s.exports}i.m=t,i.c=n,i.d=function(t,e,s){i.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:s})},i.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},i.t=function(t,e){if(1&e&&(t=i(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var s=Object.create(null);if(i.r(s),Object.defineProperty(s,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)i.d(s,n,function(e){return t[e]}.bind(null,n));return s},i.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return i.d(e,"a",e),e},i.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},i.p="/";var c=window["webpackJsonp"]=window["webpackJsonp"]||[],o=c.push.bind(c);c.push=e,c=c.slice();for(var l=0;l<c.length;l++)e(c[l]);var u=o;r.push([0,"chunk-vendors"]),s()})({0:function(t,e,s){t.exports=s("56d7")},"034f":function(t,e,s){"use strict";var n=s("64a9"),a=s.n(n);a.a},"07a4":function(t,e,s){},"12cc":function(t,e,s){"use strict";var n=s("07a4"),a=s.n(n);a.a},"14dc":function(t,e,s){var n={"./lego_black.png":"71ae","./lego_blue.png":"e6ff","./lego_brown.png":"ae22","./lego_gray.png":"2e46","./lego_green.png":"fa2a","./lego_orange.png":"ea69","./lego_red.png":"2914","./lego_unknown.png":"9011","./lego_white.png":"eb40","./lego_yellow.png":"f342"};function a(t){var e=r(t);return s(e)}function r(t){if(!s.o(n,t)){var e=new Error("Cannot find module '"+t+"'");throw e.code="MODULE_NOT_FOUND",e}return n[t]}a.keys=function(){return Object.keys(n)},a.resolve=r,t.exports=a,a.id="14dc"},2368:function(t,e,s){"use strict";var n=s("2f2c"),a=s.n(n);a.a},2699:function(t,e,s){},2914:function(t,e,s){t.exports=s.p+"img/lego_red.abcae3bb.png"},"2e46":function(t,e,s){t.exports=s.p+"img/lego_gray.8d3cc1e9.png"},"2f2c":function(t,e,s){},"32f40":function(t,e,s){"use strict";var n=s("4b0a"),a=s.n(n);a.a},"4b0a":function(t,e,s){},"56d7":function(t,e,s){"use strict";s.r(e);s("cadf"),s("551c"),s("f751"),s("097d");var n=s("2b0e"),a=s("8c4f"),r=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"app"}},[n("nav",{staticClass:"navbar navbar-expand-md navbar-light bg-light fixed-top"},[n("a",{staticClass:"navbar-brand",attrs:{href:"/"}},[n("img",{staticClass:"d-inline-block align-top",attrs:{src:s("7db1"),alt:"ETH NEXUS",height:"30"}}),t._v("\n      LEGO Sequencer v0.1\n    ")]),t._m(0),n("div",{staticClass:"collapse navbar-collapse",attrs:{id:"navbarsExampleDefault"}},[n("ul",{staticClass:"navbar-nav mr-auto"},[n("li",{staticClass:"nav-item"},[n("router-link",{staticClass:"nav-link",attrs:{to:"/",tag:"a"}},[t._v("Home")])],1),n("li",{staticClass:"nav-item"},[n("router-link",{staticClass:"nav-link",attrs:{to:"/debug",tag:"a"}},[t._v("Debug")])],1)])])]),n("main",{staticClass:"container",attrs:{role:"main"}},[n("div",{staticClass:"starter-template"},[n("router-view")],1)])])},i=[function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("button",{staticClass:"navbar-toggler",attrs:{type:"button","data-toggle":"collapse","data-target":"#navbarsExampleDefault","aria-controls":"navbarsExampleDefault","aria-expanded":"false","aria-label":"Toggle navigation"}},[s("span",{staticClass:"navbar-toggler-icon"})])}],c={name:"app",components:{}},o=c,l=(s("034f"),s("2877")),u=Object(l["a"])(o,r,i,!1,null,null,null),_=u.exports,d=s("5f5b"),p=(s("ab8b"),s("2dd8"),s("845f"),s("8634"),s("ecee")),b=s("c074"),f=s("ad3d"),v=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"steps"},[s("transition-group",{attrs:{name:"step",mode:"out-in"}},[0===t.current_step?s("div",{key:0,staticClass:"step",attrs:{id:"step1"}},[s("h1",[t._v("Welcome to the"),s("br"),t._v("LEGO Sequencer!")]),s("label",{attrs:{for:"name"}},[t._v("Please enter your name:")]),s("br"),s("input",{directives:[{name:"model",rawName:"v-model",value:t.name,expression:"name"}],attrs:{type:"text",id:"name",placeholder:"enter your name here"},domProps:{value:t.name},on:{submit:function(e){return t.proceed()},input:function(e){e.target.composing||(t.name=e.target.value)}}}),s("br"),s("button",{staticClass:"btn btn-primary",attrs:{disabled:!t.name},on:{click:function(e){return t.proceed()}}},[t._v("Continue")])]):1===t.current_step?s("div",{key:1,staticClass:"step",attrs:{id:"step2"}},[s("h1",[t._v("Scan Bricks")]),s("SingleSequencer",{attrs:{username:t.name},on:{"request-blast":t.request_blast}})],1):2===t.current_step?s("div",{key:2,staticClass:"step",attrs:{id:"step3"}},[s("h1",[t._v("BLAST Sequence")]),s("Blaster",{attrs:{sequence:t.active_sequence},on:{"results-displayed":t.blast_complete}}),t.ready_to_restart?s("div",[s("hr"),s("button",{staticClass:"btn btn-danger",on:{click:function(e){return t.restart()}}},[t._v("Start Over")])]):t._e()],1):t._e()])],1)},g=[],h=(s("7f7f"),function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("div",{staticClass:"control_tray"},[n("button",{staticClass:"btn btn-primary",attrs:{disabled:t.active_read&&!t.scan_success},on:{click:t.scan_bricks}},[t._v("\n      "+t._s(t.scan_success?"Re-scan":"Scan")+" Bricks\n    ")]),n("div",{staticClass:"status"},[t.brick_error?n("span",{staticClass:"error"},[n("b",[t._v("Error:")]),t._v(" "+t._s(t.brick_error))]):"PENDING"!==t.brick_status?n("span",["SCANNING"===t.brick_status?n("fa-icon",{attrs:{icon:"circle-notch",spin:""}}):t._e(),t._v("\n          "+t._s(t.scan_status[t.brick_status])+"\n        ")],1):t._e()])]),t.active_read?n("div",{staticClass:"brick_tray"},[n("transition-group",{attrs:{name:"bouncy"}},t._l(t.active_read,function(t,e){return n("img",{key:e,staticClass:"brick_img",attrs:{width:"35",src:s("14dc")("./lego_"+t.color+".png"),alt:t.color+" brick"}})}),0)],1):t._e(),n("transition-group",{attrs:{name:"slideup"}},[t.active_read&&t.scan_success?n("div",{key:"angle-bracket"},[n("fa-icon",{key:"arrow-bit",attrs:{icon:"angle-double-down",size:"2x"}})],1):t._e(),t.active_read&&t.scan_success?n("div",{key:"translation",staticClass:"brick_tray translation"},t._l(t.active_read,function(e,s){return n("div",{key:s,staticClass:"translated_tile align-middle"},[t._v("\n        "+t._s(t.col_to_base[e.color]||"-")+"\n      ")])}),0):t._e(),t.active_read&&t.scan_success?n("div",{key:"blast_tray",staticClass:"control_tray"},[n("button",{staticClass:"btn btn-primary",on:{click:function(e){return t.request_blast(t.active_read)}}},[t._v("BLAST Sequence")])]):t._e()])],1)}),m=[],y=s("3667"),k={green:"A",blue:"C",red:"T",yellow:"G"},C=s("8dee"),q={PENDING:"pending",SCANNING:"scanning...",ERROR:"error",COMPLETE:"done!"},S={name:"SingleSequencer",props:{username:{type:String,required:!1}},data:function(){return{brick_status:"PENDING",brick_runs:[],active_read:null,brick_error:null,blast_pending:!1,scan_status:q,col_to_base:k}},computed:{scan_success:function(){return"COMPLETE"===this.brick_status}},methods:{scan_bricks:function(){var t=this;this.brick_error=null,this.brick_status="SCANNING",y({url:"http://localhost:5000/api/query_ev3?streaming=true&username=".concat(this.username)}).start(function(){t.active_read=[]}).node("!.*",function(e){t.active_read.push(e)}).done(function(e){t.brick_status="COMPLETE"}).fail(function(e){t.active_read.push({color:"unknown"}),t.brick_status="ERROR",console.warn(e),t.brick_error=e.jsonBody&&e.jsonBody.error?e.jsonBody.error:e.body})},request_blast:function(t){var e=t.map(function(t){return k[t.color]}).join("");this.$emit("request-blast",e)}}},w=S,x=(s("b096"),Object(l["a"])(w,h,m,!1,null,"b2867f18",null)),E=x.exports,O=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[t.sequence?s("div",{staticClass:"sequence_tray list-group-item"},[t._l(t.sequence,function(e,n){return s("div",{key:n,staticClass:"translated_tile align-middle"},[t._v("\n      "+t._s(e)+"\n    ")])}),s("button",{staticClass:"btn btn-primary",staticStyle:{"white-space":"nowrap"},attrs:{disabled:t.blast_pending},on:{click:function(e){return t.blast_sequence(t.sequence)}}},[t.blast_pending?s("span",[s("fa-icon",{attrs:{icon:"circle-notch",spin:""}}),t._v("\n        Running BLAST...\n      ")],1):s("span",[t._v(t._s(t.blast_result?"Re-run":"Run")+" BLAST")])])],2):t._e(),t.blast_status||t.blast_hits?s("div",{staticClass:"status_and_results"},[s("transition-group",{attrs:{name:"slideup",mode:"out-in"}},[!t.blast_result||!t.blast_first_five||t.blast_first_five.length<=0?s("div",{key:"status_pane",staticClass:"status_pane"},[s("h4",[t._v("Status:")]),s("div",{ref:"status_scroller",staticClass:"status_scroller"},[s("transition-group",{attrs:{name:"slideright",tag:"ol"}},t._l(t.blast_status,function(e,n){return s("li",{key:n},[t._v("\n              "+t._s(e.status)+"\n              "),t.blast_pending&&n===t.blast_status.length-1?s("fa-icon",{attrs:{icon:"circle-notch",spin:""}}):t._e()],1)}),0)],1)]):t._e(),t.blast_result?s("div",{key:"results_pane",staticClass:"results_pane"},[s("div",[s("h3",{staticStyle:{"text-align":"left"}},[t._v("Hits ("+t._s(t.blast_first_five.length)+"):")]),s("hr"),t.blast_first_five.length>0?s("div",{staticClass:"species-tiles"},t._l(t.blast_first_five,function(e){return s("div",{key:e.sciname,staticClass:"species-tile"},[s("SpeciesResult",{attrs:{species:e.sciname,score:e.score,payload:e.payload},on:{"show-details":t.show_details}})],1)}),0):s("div",{staticClass:"no-results"},[t._v("\n            No matching species found.\n            "),s("br"),t._v("\n            Try again with another sequence!\n          ")])])]):t._e()])],1):t._e(),s("Sidebar",{ref:"sidedar",scopedSlots:t._u([{key:"default",fn:function(e){return t._l(e.hit.payload.hsps,function(n,a){return s("div",{staticClass:"hit-data"},[e.hit.payload.hsps.length>1?s("h4",[t._v("Hit #"+t._s(a+1))]):t._e(),s("div",{staticClass:"sec"},[s("h3",[t._v("Score:")]),s("div",{staticClass:"value"},[t._v(t._s(n.score))])]),s("div",{staticClass:"sec"},[s("h3",[t._v("Query/Hit Strand:")]),s("div",{staticClass:"value"},[t._v(t._s(n.query_strand)+" / "+t._s(n.hit_strand))])]),s("div",{staticClass:"sec"},[s("h3",[t._v("Alignment:")]),s("div",{staticClass:"value"},[s("div",{staticClass:"mini-sec"},[s("b",[t._v("Length:")]),s("br"),t._v(t._s(n.align_len)+"\n            ")]),s("div",{staticClass:"mini-sec"},[s("b",[t._v("Bases:")]),s("div",{staticClass:"alignment"},[t._v(t._s(n.qseq)+"\n                "+t._s(n.midline)+"\n                "+t._s(n.hseq)+"\n              ")])])])])])})}}])})],1)},N=[],j=(s("386d"),s("a8fc")),B=s.n(j),T=(s("8fed"),function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"card species-item",staticStyle:{width:"18rem"}},[t.species_url?s("img",{staticClass:"card-img-top",attrs:{src:t.species_url,alt:t.species}}):s("div",{staticClass:"card-img-top loading-img"},[t.loading?s("fa-icon",{attrs:{icon:"circle-notch",size:"6x",spin:""}}):t.error?s("fa-icon",{attrs:{icon:"question",size:"6x"}}):t._e()],1),s("div",{staticClass:"card-body"},[s("h5",{staticClass:"card-title"},[t._v(t._s(t.species))]),s("p",{staticClass:"card-text"},[t._v("Score: "+t._s(t.score))]),s("a",{staticClass:"btn btn-primary",attrs:{href:"#"},on:{click:function(e){return e.stopPropagation(),t.show_details(e)}}},[t._v("Details")]),t._v(" \n    "),s("a",{staticClass:"btn btn-success",attrs:{href:t.gsearch_url,target:"_blank"}},[t._v("Search "),s("fa-icon",{attrs:{icon:"external-link-alt"}})],1)])])}),P=[],L=(s("c5f6"),{name:"SpeciesResult",props:{species:{type:String,required:!0},score:{type:Number,required:!0},payload:{type:Object,required:!0}},data:function(){return{species_url:null,loading:!1,error:null}},computed:{gsearch_url:function(){return"https://www.google.com/search?safe=active&q=%22".concat(this.species,"%22")}},mounted:function(){var t=this;this.loading=!0,fetch("http://localhost:5000/api/species_img?species=".concat(this.species)).then(function(t){return t.json()}).then(function(e){if(t.loading=!1,!(e.results.length>0))throw{error:"no result found"};t.species_url=e.results[0]}).catch(function(e){t.loading=!1,t.error=e})},methods:{show_details:function(){this.$emit("show-details",{title:this.species,img_url:this.species_url,score:this.score,payload:this.payload})}}}),R=L,A=(s("7a61"),Object(l["a"])(R,T,P,!1,null,"0ce49b28",null)),$=A.exports,D=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("b-modal",{ref:"sidebar",staticClass:"modal right fade",attrs:{id:"sidebar","cancel-disabled":""},scopedSlots:t._u([{key:"modal-footer",fn:function(e){var n=e.ok;e.cancel,e.hide;return[s("b-button",{attrs:{variant:"primary"},on:{click:function(t){return n()}}},[t._v("Close")])]}}])},[s("template",{slot:"modal-title"},[s("h2",[t._v(t._s(t.display_title))])]),t.img_url?s("img",{staticClass:"img-fluid caption-img",attrs:{src:t.img_url,alt:t.display_title}}):t._e(),t.payload?s("div",{staticClass:"d-block"},[t._t("default",null,{hit:t.payload})],2):t._e()],2)},G=[],M={name:"Sidebar",props:{title:{type:String,required:!1}},data:function(){return{display_title:this.title,img_url:null,payload:null}},methods:{showModal:function(t){var e=t.title,s=t.img_url;e&&(this.display_title=e),s&&(this.img_url=s),this.payload=t,console.log(t),this.$refs.sidebar.show()}}},I=M,H=(s("32f40"),Object(l["a"])(I,D,G,!1,null,"6b939d07",null)),U=H.exports,z={name:"Blaster",components:{Sidebar:U,SpeciesResult:$},props:{sequence:{type:String,required:!1}},data:function(){return{blast_pending:!1,blast_status:null,blast_result:null}},mounted:function(){this.sequence&&this.blast_sequence(this.sequence)},computed:{blast_hits:function(){return this.blast_result?this.blast_result.data.BlastOutput2[0].report.results.search.hits.map(function(t){return{sciname:t.description[0].sciname,score:t.hsps[0].score,payload:t}}):null},blast_unique_hits:function(){return this.blast_hits?B()(this.blast_hits,function(t){return t.sciname}):null},blast_first_five:function(){return this.blast_unique_hits?this.blast_unique_hits.slice(0,6):null}},methods:{blast_sequence:function(t){var e=this;console.log("BLASTing ",t),y("http://localhost:5000/api/blast?sequence=".concat(t)).start(function(){e.blast_pending=!0,e.blast_result=null,e.blast_status=[{status:"BLASTing ".concat(t,"...")}]}).node("!.{status}",function(t){console.log(t),e.blast_status.push(t);var s=e.$refs.status_scroller;s&&setTimeout(function(){s.scrollTop=s.scrollHeight},10)}).node("!.{results}",function(s){console.log("Done: ",s),e.blast_result={sequence:t,data:s.results}}).done(function(){e.blast_pending=!1,e.$emit("results-displayed")}).fail(function(t){e.blast_status.push({status:"Error occurred during request, terminated."}),e.blast_pending=!1})},show_details:function(t){this.$refs.sidedar.showModal(t)}}},F=z,J=(s("2368"),Object(l["a"])(F,O,N,!1,null,"3faea39d",null)),Q=J.exports,W={name:"Process",components:{Blaster:Q,SingleSequencer:E},data:function(){return{name:"",current_step:0,active_sequence:null,ready_to_restart:!1}},methods:{restart:function(){var t=this;this.current_step=99,window.scroll({top:0,left:0,behavior:"smooth"}),setTimeout(function(){t.name="",t.current_step=0,t.active_sequence=null,t.ready_to_restart=!1},300)},proceed:function(){0===this.current_step?this.name&&(this.current_step=1):1===this.current_step&&this.active_sequence&&(this.current_step=2)},request_blast:function(t){this.active_sequence=t,this.proceed()},blast_complete:function(){console.log("BLAST done!"),this.ready_to_restart=!0}}},X=W,K=(s("12cc"),Object(l["a"])(X,v,g,!1,null,"7b48b970",null)),V=K.exports,Y=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("h1",[t._v("LEGO Sequencer (Debug)")]),s("div",{staticClass:"step"},[s("h2",[t._v("1. Nudge Controls")]),s("div",{staticClass:"controls",staticStyle:{"align-items":"baseline"}},[s("button",{staticClass:"btn btn-sm btn-primary",on:{click:function(e){return t.nudge("left",t.nudge_amount)}}},[t._v("« nudge left")]),s("button",{staticClass:"btn btn-sm btn-primary",on:{click:function(e){return t.nudge("right",t.nudge_amount)}}},[t._v("nudge right »")]),s("label",[t._v("Bricks:\n        "),s("input",{directives:[{name:"model",rawName:"v-model",value:t.nudge_amount,expression:"nudge_amount"}],attrs:{type:"number",name:"amount"},domProps:{value:t.nudge_amount},on:{input:function(e){e.target.composing||(t.nudge_amount=e.target.value)}}})])]),s("div",{staticClass:"results"},[t._v("\n      "+t._s(t.response)+"\n    ")])])])},Z=[];function tt(t){if(!t.ok&&t.error)throw console.warn("Failed: ",t),t;return t}var et={name:"Debug",data:function(){return{nudge_amount:1,response:"..."}},methods:{ping:function(){var t=this;fetch("http://localhost:5000/api/ping").then(function(t){return t.json()}).then(function(e){t.response=e.msg})},nudge:function(t,e){var s=this;fetch("http://localhost:5000/api/nudge/".concat(t,"/").concat(e)).then(tt).then(function(t){return t.json()}).then(function(t){s.response=t.msg}).catch(function(t){s.response=t})}}},st=et,nt=Object(l["a"])(st,Y,Z,!1,null,"947947b4",null),at=nt.exports,rt=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("div",[s("h2",[t._v("Scan Sequence")]),s("Sequencer",{on:{"request-blast":t.request_blast}})],1),s("div",[s("h2",[t._v("BLAST Results")]),s("Blaster",{attrs:{sequence:t.active_sequence}})],1)])},it=[],ct=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"step"},[n("div",{staticClass:"controls"},[n("button",{staticClass:"btn btn-primary",attrs:{disabled:t.active_read},on:{click:t.scan_bricks}},[t._v("scan bricks")]),n("button",{staticClass:"btn btn-danger",on:{click:t.clear_all}},[t._v("clear runs")]),n("span",{staticClass:"status"},[t.brick_error?n("span",{staticClass:"error"},[n("b",[t._v("Error:")]),t._v(" "+t._s(t.brick_error))]):n("span",["SCANNING"===t.brick_status?n("fa-icon",{attrs:{icon:"spinner",pulse:""}}):t._e(),t._v("\n          "+t._s(t.scan_status[t.brick_status])+"\n        ")],1)])]),n("ul",{staticClass:"list-group",staticStyle:{"margin-top":"1em"}},[t._l(t.brick_runs,function(e,a){return n("li",{key:e.name,class:"list-group-item brick_run "+(e.name==t.selected_run?"selected":"")},[n("div",{staticClass:"seq_brick_tray"},[n("button",{staticClass:"blaster-btn btn-sm btn btn-danger",on:{click:function(s){return t.remove_sequence(e.name)}}},[n("fa-icon",{attrs:{icon:"trash"}})],1),n("button",{staticClass:"blaster-btn btn-sm btn btn-primary",on:{click:function(s){return t.request_blast(e.name)}}},[t._v("BLAST")]),t._l(e.data,function(t,e){return n("img",{key:e,staticClass:"brick_img",attrs:{width:"30",src:s("14dc")("./lego_"+t.color+".png")}})})],2)])}),t.active_read?n("li",{staticClass:"list-group-item brick_run active_read"},[n("div",{staticClass:"brick_tray"},[n("button",{staticClass:"blaster-btn btn-sm btn btn-secondary",attrs:{disabled:""}},[n("fa-icon",{attrs:{icon:"trash"}})],1),n("button",{staticClass:"blaster-btn btn-sm btn btn-secondary",attrs:{disabled:""}},[t._v("BLAST")]),t._l(t.active_read,function(t,e){return n("img",{key:e,staticClass:"brick_img",attrs:{width:"30",src:s("14dc")("./lego_"+t.color+".png")}})})],2)]):t._e()],2)])},ot=[],lt=(s("7514"),{PENDING:"pending",SCANNING:"scanning...",ERROR:"error",COMPLETE:"done!"}),ut={name:"Sequencer",data:function(){return{brick_status:"PENDING",brick_runs:[],active_read:null,brick_error:null,blast_pending:!1,scan_status:lt,selected_run:null}},methods:{scan_bricks:function(){var t=this;this.brick_error=null,this.brick_status="SCANNING",y({url:"http://localhost:5000/api/query_ev3?streaming=true"}).start(function(){t.active_read=[]}).node("!.*",function(e){t.active_read.push(e)}).done(function(e){t.brick_status="COMPLETE",t.brick_runs.push({name:Object(C["generate"])(),data:e}),t.active_read=null}).fail(function(e){t.active_read.push({color:"unknown"}),t.brick_status="ERROR",console.warn(e),t.brick_error=e.jsonBody&&e.jsonBody.error?e.jsonBody.error:e.body})},remove_sequence:function(t){confirm("Remove this entry?")&&(this.brick_runs=this.brick_runs.filter(function(e){return e.name!==t}),this.selected_run===t&&(this.selected_run=null))},clear_all:function(){confirm("Clear all entries?")&&(this.brick_runs=[],this.selected_run=null)},request_blast:function(t){var e=this.brick_runs.find(function(e){return e.name===t});if(e){this.selected_run=t;var s=e.data.map(function(t){return k[t.color]}).join("");this.$emit("request-blast",s)}else alert("Unable to find sequence with name ".concat(t,"!"))}}},_t=ut,dt=(s("806a"),Object(l["a"])(_t,ct,ot,!1,null,"7a56728c",null)),pt=dt.exports,bt={name:"Home",components:{Blaster:Q,Sequencer:pt},data:function(){return{active_sequence:null}},methods:{request_blast:function(t){console.log("BLAST requested: ",t),this.active_sequence=t}}},ft=bt,vt=Object(l["a"])(ft,rt,it,!1,null,"0240b25a",null),gt=vt.exports;n["default"].config.productionTip=!1,n["default"].use(d["a"]),p["c"].add(b["h"],b["f"],b["g"],b["b"],b["a"],b["d"],b["e"],b["c"]),n["default"].component("fa-icon",f["a"]),n["default"].use(a["a"]);var ht=new a["a"]({mode:"history",routes:[{path:"/",component:V,name:"home"},{path:"/debug",component:at,name:"debug"},{path:"/designer",component:gt,name:"designer"}]});new n["default"]({render:function(t){return t(_)},router:ht}).$mount("#app")},"64a9":function(t,e,s){},"71ae":function(t,e,s){t.exports=s.p+"img/lego_black.e0a5cc99.png"},"73ce":function(t,e,s){},"7a61":function(t,e,s){"use strict";var n=s("2699"),a=s.n(n);a.a},"7db1":function(t,e,s){t.exports=s.p+"img/nexus_icon.ebd95bd1.png"},"806a":function(t,e,s){"use strict";var n=s("be9b"),a=s.n(n);a.a},"845f":function(t,e,s){},8634:function(t,e,s){},9011:function(t,e,s){t.exports=s.p+"img/lego_unknown.dd4533c5.png"},ae22:function(t,e,s){t.exports=s.p+"img/lego_brown.e0a9636d.png"},b096:function(t,e,s){"use strict";var n=s("73ce"),a=s.n(n);a.a},be9b:function(t,e,s){},e6ff:function(t,e,s){t.exports=s.p+"img/lego_blue.55fcb86d.png"},ea69:function(t,e,s){t.exports=s.p+"img/lego_orange.e7ba1561.png"},eb40:function(t,e,s){t.exports=s.p+"img/lego_white.3d50df46.png"},f342:function(t,e,s){t.exports=s.p+"img/lego_yellow.31595d79.png"},fa2a:function(t,e,s){t.exports=s.p+"img/lego_green.4179fe81.png"}});
//# sourceMappingURL=app.15b43e8d.js.map