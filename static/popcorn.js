/*
 * popcorn.js version v1.5.11
 * http://popcornjs.org
 *
 * Copyright 2011, Mozilla Foundation
 * Licensed under the MIT license
 */

!function(){if(!document.addEventListener&&!document.removeEventListener&&!document.dispatchEvent){var t={},e=function(e,n){return e="DOMContentLoaded"===e?"readystatechange":e,Event[e.toUpperCase()]||"readystatechange"===e?void document.attachEvent("on"+e,n):(t[e]||(t[e]={events:[],queue:[],active:!1}),void(t[e].active?t[e].queue.push(n):t[e].events.push(n)))},n=function(e,n){e="DOMContentLoaded"===e?"readystatechange":e;var r=0,a=t[e];if(Event[e.toUpperCase()]||"readystatechange"===e)return void document.detachEvent("on"+e,n);if(a){for(r=a.events.length-1;r>=0;r--)n===a.events[r]&&delete a.events[r];for(r=a.queue.length-1;r>=0;r--)n===a.queue[r]&&delete a.queue[r]}},r=function(e){var n,r,a,i,o=this,s=e.type;if(s||(s=e,r=Popcorn.events.getInterface(s),r&&(n=document.createEvent(r),n.initCustomEvent(s,!0,!0,window,1))),a=t[s]){a.active=!0;for(var d=0;d<a.events.length;d++)a.events[d]&&a.events[d].call(o,n,o);if(a.queue.length)for(;a.queue.length;)i=a.queue.shift(),i&&a.events.push(i);a.active=!1,a.events.forEach(function(t){t||a.events.splice(a.events.indexOf(t),1)}),a.queue.forEach(function(t){t||a.queue.splice(a.queue.indexOf(t),1)})}};document.addEventListener=e,document.removeEventListener=n,document.dispatchEvent=r}Event.prototype.preventDefault||(Event.prototype.preventDefault=function(){this.returnValue=!1}),Event.prototype.stopPropagation||(Event.prototype.stopPropagation=function(){this.cancelBubble=!0}),window.addEventListener=window.addEventListener||function(t,e){t="on"+t,window.attachEvent(t,e)},window.removeEventListener=window.removeEventListener||function(t,e){t="on"+t,window.detachEvent(t,e)},HTMLScriptElement.prototype.addEventListener=HTMLScriptElement.prototype.addEventListener||function(t,e){t="load"===t?"onreadystatechange":"on"+t,"onreadystatechange"===t&&(e.readyStateCheck=e.readyStateCheck||function(t){"loaded"===self.readyState&&e(t)}),this.attachEvent(t,e.readyStateCheck||e)},HTMLScriptElement.prototype.removeEventListener=HTMLScriptElement.prototype.removeEventListener||function(t,e){t="load"===t?"onreadystatechange":"on"+t,this.detachEvent(t,e.readyStateCheck||e)},document.createEvent=document.createEvent||function(t){return{type:null,target:null,currentTarget:null,cancelable:!1,detail:!1,bubbles:!1,initEvent:function(t,e,n){this.type=t},initCustomEvent:function(t,e,n,r){this.type=t,this.detail=r},stopPropagation:function(){},stopImmediatePropagation:function(){}}},Array.prototype.forEach=Array.prototype.forEach||function(t,e){var n=this,r=Object.prototype.hasOwnProperty;if(!n||!t)return{};e=e||this;var a;for(a in n)r.call(n,a)&&t.call(e,n[a],a,n);return n},Array.prototype.map||(Array.prototype.map=function(t,e){var n,r,a;if(null==this)throw new TypeError("this is null or not defined");var i=Object(this),o=i.length>>>0;if("[object Function]"!={}.toString.call(t))throw new TypeError(t+" is not a function");for(e&&(n=e),r=new Array(o),a=0;o>a;){var s,d;a in i&&(s=i[a],d=t.call(n,s,a,i),r[a]=d),a++}return r}),Array.prototype.indexOf||(Array.prototype.indexOf=function(t){if(null==this)throw new TypeError;var e=Object(this),n=e.length>>>0;if(0===n)return-1;var r=0;if(arguments.length>0&&(r=Number(arguments[1]),r!=r?r=0:0!=r&&r!=1/0&&r!=-(1/0)&&(r=(r>0||-1)*Math.floor(Math.abs(r)))),r>=n)return-1;for(var a=r>=0?r:Math.max(n-Math.abs(r),0);n>a;a++)if(a in e&&e[a]===t)return a;return-1}),"function"!=typeof String.prototype.trim&&(String.prototype.trim=function(){return this.replace(/^\s+|\s+$/g,"")}),Object.keys||(Object.keys=function(){"use strict";var t=Object.prototype.hasOwnProperty,e=!{toString:null}.propertyIsEnumerable("toString"),n=["toString","toLocaleString","valueOf","hasOwnProperty","isPrototypeOf","propertyIsEnumerable","constructor"],r=n.length;return function(a){if("object"!=typeof a&&("function"!=typeof a||null===a))throw new TypeError("Object.keys called on non-object");var i,o,s=[];for(i in a)t.call(a,i)&&s.push(i);if(e)for(o=0;r>o;o++)t.call(a,n[o])&&s.push(n[o]);return s}}()),Object.defineProperties||(Object.defineProperties=function(t,e){function n(e){function n(t,e){return Object.prototype.hasOwnProperty.call(t,e)}function r(t){return"function"==typeof t}if("object"!=typeof e||null===e)throw new TypeError("bad desc");var a={};if(n(e,"enumerable")&&(a.enumerable=!!t.enumerable),n(e,"configurable")&&(a.configurable=!!e.configurable),n(e,"value")&&(a.value=t.value),n(e,"writable")&&(a.writable=!!e.writable),n(e,"get")){var i=e.get;if(!r(i)&&"undefined"!==i)throw new TypeError("bad get");a.get=i}if(n(e,"set")){var o=e.set;if(!r(o)&&"undefined"!==o)throw new TypeError("bad set");a.set=o}if(("get"in a||"set"in a)&&("value"in a||"writable"in a))throw new TypeError("identity-confused descriptor");return a}if("object"!=typeof t||null===t)throw new TypeError("bad obj");e=Object(e);for(var r=Object.keys(e),a=[],i=0;i<r.length;i++)a.push([r[i],n(e[r[i]])]);for(var i=0;i<a.length;i++)Object.defineProperty(t,a[i][0],a[i][1]);return t})}(),function(t,e){function n(t){_.put.call(this,t)}function r(t){this.parent=t,this.byStart=[{start:-1,end:-1}],this.byEnd=[{start:-1,end:-1}],this.animating=[],this.startIndex=0,this.endIndex=0,this.previousUpdateTime=-1,this.count=1}function a(t,e,n){return t[e]&&t[e]===n}function i(t,e){var n={};for(var r in t)l.call(e,r)&&l.call(t,r)&&(n[r]=t[r]);return n}function o(t,e){return function(){if(b.plugin.debug)return t.apply(this,arguments);try{return t.apply(this,arguments)}catch(n){b.plugin.errors.push({plugin:e,thrown:n,source:t.toString()}),this.emit("pluginerror",b.plugin.errors)}}}if(e.addEventListener){var s=Array.prototype,d=Object.prototype,u=s.forEach,c=s.slice,l=d.hasOwnProperty,p=d.toString,f=t.Popcorn,h=[],v=!1,y=!1,m={events:{hash:{},apis:{}}},g=function(){return t.requestAnimationFrame||t.webkitRequestAnimationFrame||t.mozRequestAnimationFrame||t.oRequestAnimationFrame||t.msRequestAnimationFrame||function(e,n){t.setTimeout(e,16)}}(),E=function(t){return Object.keys?Object.keys(t):function(t){var e,n=[];for(e in t)l.call(t,e)&&n.push(e);return n}(t)},_={put:function(t){for(var e in t)t.hasOwnProperty(e)&&(this[e]=t[e])}},b=function(t,e){return new b.p.init(t,e||null)};b.version="@VERSION",b.isSupported=!0,b.instances=[],b.p=b.prototype={init:function(t,n){var a,i,o=this;{if("function"!=typeof t){if("string"==typeof t)try{a=e.querySelector(t)}catch(s){throw new Error("Popcorn.js Error: Invalid media element selector: "+t)}if(this.media=a||t,i=this.media.nodeName&&this.media.nodeName.toLowerCase()||"video",this[i]=this.media,this.options=b.extend({},n)||{},this.id=this.options.id||b.guid(i),b.byId(this.id))throw new Error("Popcorn.js Error: Cannot use duplicate ID ("+this.id+")");this.isDestroyed=!1,this.data={running:{cue:[]},timeUpdate:b.nop,disabled:{},events:{},hooks:{},history:[],state:{volume:this.media.volume},trackRefs:{},trackEvents:new r(this)},b.instances.push(this);var d=function(){o.media.currentTime<0&&(o.media.currentTime=0),o.media.removeEventListener("loadedmetadata",d,!1);var t,e,n,r,a,i;t=o.media.duration,e=t!=t?Number.MAX_VALUE:t+1,b.addTrackEvent(o,{start:e,end:e}),o.isDestroyed||(o.data.durationChange=function(){var t=o.media.duration,e=t+1,n=o.data.trackEvents.byStart,r=o.data.trackEvents.byEnd;n.pop(),r.pop();for(var a=r.length-1;a>0;a--)r[a].end>t&&o.removeTrackEvent(r[a]._id);for(var i=0;i<n.length;i++)n[i].end>t&&o.removeTrackEvent(n[i]._id);o.data.trackEvents.byEnd.push({start:e,end:e}),o.data.trackEvents.byStart.push({start:e,end:e})},o.media.addEventListener("durationchange",o.data.durationChange,!1)),o.options.frameAnimation?(o.data.timeUpdate=function(){b.timeUpdate(o,{}),b.forEach(b.manifest,function(t,e){if(n=o.data.running[e]){a=n.length;for(var s=0;a>s;s++)r=n[s],i=r._natives,i&&i.frame&&i.frame.call(o,{},r,o.currentTime())}}),o.emit("timeupdate"),!o.isDestroyed&&g(o.data.timeUpdate)},!o.isDestroyed&&g(o.data.timeUpdate)):(o.data.timeUpdate=function(t){b.timeUpdate(o,t)},o.isDestroyed||o.media.addEventListener("timeupdate",o.data.timeUpdate,!1))};return o.media.addEventListener("error",function(){o.error=o.media.error},!1),o.media.readyState>=1?d():o.media.addEventListener("loadedmetadata",d,!1),this}if("complete"===e.readyState)return void t(e,b);if(h.push(t),!v){v=!0;var u=function(){y=!0,e.removeEventListener("DOMContentLoaded",u,!1);for(var t=0,n=h.length;n>t;t++)h[t].call(e,b);h=null};e.addEventListener("DOMContentLoaded",u,!1)}}}},b.p.init.prototype=b.p,b.byId=function(t){for(var e=b.instances,n=e.length,r=0;n>r;r++)if(e[r].id===t)return e[r];return null},b.forEach=function(t,e,n){if(!t||!e)return{};n=n||this;var r,a;if(u&&t.forEach===u)return t.forEach(e,n);if("[object NodeList]"===p.call(t)){for(r=0,a=t.length;a>r;r++)e.call(n,t[r],r,t);return t}for(r in t)l.call(t,r)&&e.call(n,t[r],r,t);return t},b.extend=function(t){var e=t,n=c.call(arguments,1);return b.forEach(n,function(t){for(var n in t)e[n]=t[n]}),e},b.extend(b,{noConflict:function(e){return e&&(t.Popcorn=f),b},error:function(t){throw new Error(t)},guid:function(t){return b.guid.counter++,(t?t:"")+(+new Date+b.guid.counter)},sizeOf:function(t){var e=0;for(var n in t)e++;return e},isArray:Array.isArray||function(t){return"[object Array]"===p.call(t)},nop:function(){},position:function(n){if(!n.parentNode)return null;var r,a,i,o,s,d,u=n.getBoundingClientRect(),c={},l=(n.ownerDocument,e.documentElement),p=e.body;r=l.clientTop||p.clientTop||0,a=l.clientLeft||p.clientLeft||0,i=t.pageYOffset&&l.scrollTop||p.scrollTop,o=t.pageXOffset&&l.scrollLeft||p.scrollLeft,s=Math.ceil(u.top+i-r),d=Math.ceil(u.left+o-a);for(var f in u)c[f]=Math.round(u[f]);return b.extend({},c,{top:s,left:d})},disable:function(t,e){if(!t.data.disabled[e]){if(t.data.disabled[e]=!0,e in b.registryByName&&t.data.running[e])for(var n,r=t.data.running[e].length-1;r>=0;r--)n=t.data.running[e][r],n._natives.end.call(t,null,n),t.emit("trackend",b.extend({},n,{plugin:n.type,type:"trackend"}));return t}},enable:function(t,e){if(t.data.disabled[e]){if(t.data.disabled[e]=!1,e in b.registryByName&&t.data.running[e])for(var n,r=t.data.running[e].length-1;r>=0;r--)n=t.data.running[e][r],n._natives.start.call(t,null,n),t.emit("trackstart",b.extend({},n,{plugin:n.type,type:"trackstart",track:n}));return t}},destroy:function(t){var e,n,r,a,i=t.data.events,o=t.data.trackEvents;for(n in i){e=i[n];for(r in e)delete e[r];i[n]=null}for(a in b.registryByName)b.removePlugin(t,a);o.byStart.length=0,o.byEnd.length=0,t.isDestroyed||(t.data.timeUpdate&&t.media.removeEventListener("timeupdate",t.data.timeUpdate,!1),t.isDestroyed=!0),b.instances.splice(b.instances.indexOf(t),1)}}),b.guid.counter=1,b.extend(b.p,function(){var t="load play pause currentTime playbackRate volume duration preload playbackRate autoplay loop controls muted buffered readyState seeking paused played seekable ended",e={};return b.forEach(t.split(/\s+/g),function(t){e[t]=function(e){var n;return"function"==typeof this.media[t]?(null!=e&&/play|pause/.test(t)&&(this.media.currentTime=b.util.toSeconds(e)),this.media[t](),this):null!=e?(n=this.media[t],this.media[t]=e,n!==e&&this.emit("attrchange",{attribute:t,previousValue:n,currentValue:e}),this):this.media[t]}}),e}()),b.forEach("enable disable".split(" "),function(t){b.p[t]=function(e){return b[t](this,e)}}),b.extend(b.p,{roundTime:function(){return Math.round(this.media.currentTime)},exec:function(t,e,r){var a,i,o,s=arguments.length,d="trackadded";try{i=b.util.toSeconds(t)}catch(u){}if("number"==typeof i&&(t=i),"number"==typeof t&&2===s)r=e,e=t,t=b.guid("cue");else if(1===s)e=-1;else if(a=this.getTrackEvent(t))this.data.trackEvents.remove(t),n.end(this,a),b.removeTrackEvent.ref(this,t),d="cuechange","string"==typeof t&&2===s&&("number"==typeof e&&(r=a._natives.start),"function"==typeof e&&(r=e,e=a.start));else if(s>=2){if("string"==typeof e){try{i=b.util.toSeconds(e)}catch(u){}e=i}"number"==typeof e&&(r=r||b.nop()),"function"==typeof e&&(r=e,e=-1)}return o={id:t,start:e,end:e+1,_running:!1,_natives:{start:r||b.nop,end:b.nop,type:"cue"}},a&&(o=b.extend(a,o)),"cuechange"===d?(o._id=o.id||o._id||b.guid(o._natives.type),this.data.trackEvents.add(o),n.start(this,o),this.timeUpdate(this,null,!0),b.addTrackEvent.ref(this,o),this.emit(d,b.extend({},o,{id:t,type:d,previousValue:{time:a.start,fn:a._natives.start},currentValue:{time:e,fn:r||b.nop},track:a}))):b.addTrackEvent(this,o),this},mute:function(t){var e=null==t||t===!0?"muted":"unmuted";return"unmuted"===e&&(this.media.muted=!1,this.media.volume=this.data.state.volume),"muted"===e&&(this.data.state.volume=this.media.volume,this.media.muted=!0),this.emit(e),this},unmute:function(t){return this.mute(null==t?!1:!t)},position:function(){return b.position(this.media)},toggle:function(t){return b[this.data.disabled[t]?"enable":"disable"](this,t)},defaults:function(t,e){return b.isArray(t)?(b.forEach(t,function(t){for(var e in t)this.defaults(e,t[e])},this),this):(this.options.defaults||(this.options.defaults={}),this.options.defaults[t]||(this.options.defaults[t]={}),b.extend(this.options.defaults[t],e),this)}}),b.Events={UIEvents:"blur focus focusin focusout load resize scroll unload",MouseEvents:"mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave click dblclick",Events:"loadstart progress suspend emptied stalled play pause error loadedmetadata loadeddata waiting playing canplay canplaythrough seeking seeked timeupdate ended ratechange durationchange volumechange"},b.Events.Natives=b.Events.UIEvents+" "+b.Events.MouseEvents+" "+b.Events.Events,m.events.apiTypes=["UIEvents","MouseEvents","Events"],function(t,e){for(var n=m.events.apiTypes,r=t.Natives.split(/\s+/g),a=0,i=r.length;i>a;a++)e.hash[r[a]]=!0;n.forEach(function(n,r){e.apis[n]={};for(var a=t[n].split(/\s+/g),i=a.length,o=0;i>o;o++)e.apis[n][a[o]]=!0})}(b.Events,m.events),b.events={isNative:function(t){return!!m.events.hash[t]},getInterface:function(t){if(!b.events.isNative(t))return!1;for(var e,n,r=m.events,a=r.apiTypes,i=r.apis,o=0,s=a.length;s>o;o++)if(n=a[o],i[n][t]){e=n;break}return e},all:b.Events.Natives.split(/\s+/g),fn:{trigger:function(n,r){var a,i,o,s=this.data.events[n];if(s){if(a=b.events.getInterface(n))return i=e.createEvent(a),i.initEvent(n,!0,!0,t,1),this.media.dispatchEvent(i),this;for(o=s.slice();o.length;)o.shift().call(this,r)}return this},listen:function(t,e){var n,r,a=this,i=!0,o=b.events.hooks[t];if("function"!=typeof e)throw new Error("Popcorn.js Error: Listener is not a function");return this.data.events[t]||(this.data.events[t]=[],i=!1),o&&(o.add&&o.add.call(this,{},e),o.bind&&(t=o.bind),o.handler&&(r=e,e=function(t){o.handler.call(a,t,r)}),i=!0,this.data.events[t]||(this.data.events[t]=[],i=!1)),this.data.events[t].push(e),!i&&b.events.all.indexOf(t)>-1&&this.media.addEventListener(t,function(e){if(a.data.events[t])for(n=a.data.events[t].slice();n.length;)n.shift().call(a,e)},!1),this},unlisten:function(t,e){var n,r=this.data.events[t];if(r){if("string"==typeof e){for(var a=0;a<r.length;a++)r[a].name===e&&r.splice(a--,1);return this}if("function"==typeof e){for(;-1!==n;)n=r.indexOf(e),-1!==n&&r.splice(n,1);return this}return this.data.events[t]=null,this}}},hooks:{canplayall:{bind:"canplaythrough",add:function(t,e){var n=!1;this.media.readyState&&(setTimeout(function(){e.call(this,t)}.bind(this),0),n=!0),this.data.hooks.canplayall={fired:n}},handler:function(t,e){this.data.hooks.canplayall.fired||(e.call(this,t),this.data.hooks.canplayall.fired=!0)}}}},b.forEach([["trigger","emit"],["listen","on"],["unlisten","off"]],function(t){b.p[t[0]]=b.p[t[1]]=b.events.fn[t[0]]}),n.start=function(t,e){e.end>t.media.currentTime&&e.start<=t.media.currentTime&&!e._running&&(e._running=!0,t.data.running[e._natives.type].push(e),t.data.disabled[e._natives.type]||(e._natives.start.call(t,null,e),t.emit("trackstart",b.extend({},e,{plugin:e._natives.type,type:"trackstart",track:e}))))},n.end=function(t,e){var n;(e.end<=t.media.currentTime||e.start>t.media.currentTime)&&e._running&&(n=t.data.running[e._natives.type],e._running=!1,n.splice(n.indexOf(e),1),t.data.disabled[e._natives.type]||(e._natives.end.call(t,null,e),t.emit("trackend",b.extend({},e,{plugin:e._natives.type,type:"trackend",track:e}))))},r.prototype.where=function(t){return(this.parent.getTrackEvents()||[]).filter(function(e){var n,r;if(!t)return!0;for(n in t)if(r=t[n],a(e,n,r)||a(e._natives,n,r))return!0;return!1})},r.prototype.add=function(t){var e,n,r=this.byStart,a=this.byEnd;for(t&&t._id&&this.parent.data.history.push(t._id),t.start=b.util.toSeconds(t.start,this.parent.options.framerate),t.end=b.util.toSeconds(t.end,this.parent.options.framerate),e=r.length-1;e>=0;e--)if(t.start>=r[e].start){r.splice(e+1,0,t);break}for(n=a.length-1;n>=0;n--)if(t.end>a[n].end){a.splice(n+1,0,t);break}e<=this.parent.data.trackEvents.startIndex&&t.start<=this.parent.data.trackEvents.previousUpdateTime&&this.parent.data.trackEvents.startIndex++,n<=this.parent.data.trackEvents.endIndex&&t.end<this.parent.data.trackEvents.previousUpdateTime&&this.parent.data.trackEvents.endIndex++,this.count++},r.prototype.remove=function(t,e){if(t instanceof n&&(t=t.id),"object"==typeof t)return this.where(t).forEach(function(t){this.removeTrackEvent(t._id)},this.parent),this;var r,a,i,o,s,d=this.byStart.length,u=0,c=0,l=[],p=[],f=[],h=[];for(e=e||{};--d>-1;)r=this.byStart[u],a=this.byEnd[u],r._id||(l.push(r),p.push(a)),r._id&&(r._id!==t&&l.push(r),a._id!==t&&p.push(a),r._id===t&&(c=u,s=r)),u++;if(d=this.animating.length,u=0,d)for(;--d>-1;)i=this.animating[u],i._id||f.push(i),i._id&&i._id!==t&&f.push(i),u++;c<=this.startIndex&&this.startIndex--,c<=this.endIndex&&this.endIndex--,this.byStart=l,this.byEnd=p,this.animating=f,this.count--,o=this.parent.data.history.length;for(var v=0;o>v;v++)this.parent.data.history[v]!==t&&h.push(this.parent.data.history[v]);this.parent.data.history=h},b.addTrackEvent=function(t,e){var r;e instanceof n||(e=new n(e),e&&e._natives&&e._natives.type&&t.options.defaults&&t.options.defaults[e._natives.type]&&(r=b.extend({},e),b.extend(e,t.options.defaults[e._natives.type],r)),e._natives&&(e._id=e.id||e._id||b.guid(e._natives.type),e._natives._setup&&(e._natives._setup.call(t,e),t.emit("tracksetup",b.extend({},e,{plugin:e._natives.type,type:"tracksetup",track:e})))),t.data.trackEvents.add(e),n.start(t,e),this.timeUpdate(t,null,!0),e._id&&b.addTrackEvent.ref(t,e),t.emit("trackadded",b.extend({},e,e._natives?{plugin:e._natives.type}:{},{type:"trackadded",track:e})))},b.addTrackEvent.ref=function(t,e){return t.data.trackRefs[e._id]=e,t},b.removeTrackEvent=function(t,e){var n=t.getTrackEvent(e);n&&(n._natives._teardown&&n._natives._teardown.call(t,n),t.data.trackEvents.remove(e),b.removeTrackEvent.ref(t,e),n._natives&&t.emit("trackremoved",b.extend({},n,{plugin:n._natives.type,type:"trackremoved",track:n})))},b.removeTrackEvent.ref=function(t,e){return delete t.data.trackRefs[e],t},b.getTrackEvents=function(t){for(var e,n=[],r=t.data.trackEvents.byStart,a=r.length,i=0;a>i;i++)e=r[i],e._id&&n.push(e);return n},b.getTrackEvents.ref=function(t){return t.data.trackRefs},b.getTrackEvent=function(t,e){return t.data.trackRefs[e]},b.getTrackEvent.ref=function(t,e){return t.data.trackRefs[e]},b.getLastTrackEventId=function(t){return t.data.history[t.data.history.length-1]},b.timeUpdate=function(t,e){var n,r,a,i,o,s=t.media.currentTime,d=t.data.trackEvents.previousUpdateTime,u=t.data.trackEvents,c=u.endIndex,l=u.startIndex,p=u.byStart.length,f=u.byEnd.length,h=b.registryByName,v="trackstart",y="trackend";if(s>=d){for(;u.byEnd[c]&&u.byEnd[c].end<=s;){if(n=u.byEnd[c],a=n._natives,i=a&&a.type,a&&!h[i]&&!t[i])return void b.removeTrackEvent(t,n._id);n._running===!0&&(n._running=!1,o=t.data.running[i],o.splice(o.indexOf(n),1),t.data.disabled[i]||(a.end.call(t,e,n),t.emit(y,b.extend({},n,{plugin:i,type:y,track:n})))),c++}for(;u.byStart[l]&&u.byStart[l].start<=s;){if(r=u.byStart[l],a=r._natives,i=a&&a.type,a&&!h[i]&&!t[i])return void b.removeTrackEvent(t,r._id);r.end>s&&r._running===!1&&(r._running=!0,t.data.running[i].push(r),t.data.disabled[i]||(a.start.call(t,e,r),t.emit(v,b.extend({},r,{plugin:i,type:v,track:r})))),l++}}else if(d>s){for(;u.byStart[l]&&u.byStart[l].start>s;){if(r=u.byStart[l],a=r._natives,i=a&&a.type,a&&!h[i]&&!t[i])return void b.removeTrackEvent(t,r._id);r._running===!0&&(r._running=!1,o=t.data.running[i],o.splice(o.indexOf(r),1),t.data.disabled[i]||(a.end.call(t,e,r),t.emit(y,b.extend({},r,{plugin:i,type:y,track:r})))),l--}for(;u.byEnd[c]&&u.byEnd[c].end>s;){if(n=u.byEnd[c],a=n._natives,i=a&&a.type,a&&!h[i]&&!t[i])return void b.removeTrackEvent(t,n._id);n.start<=s&&n._running===!1&&(n._running=!0,t.data.running[i].push(n),t.data.disabled[i]||(a.start.call(t,e,n),t.emit(v,b.extend({},n,{plugin:i,type:v,track:n})))),c--}}u.endIndex=c,u.startIndex=l,u.previousUpdateTime=s,u.byStart.length<p&&u.startIndex--,u.byEnd.length<f&&u.endIndex--},b.extend(b.p,{getTrackEvents:function(){return b.getTrackEvents.call(null,this)},getTrackEvent:function(t){return b.getTrackEvent.call(null,this,t)},getLastTrackEventId:function(){return b.getLastTrackEventId.call(null,this)},removeTrackEvent:function(t){return b.removeTrackEvent.call(null,this,t),this},removePlugin:function(t){return b.removePlugin.call(null,this,t),this},timeUpdate:function(t){return b.timeUpdate.call(null,this,t),this},destroy:function(){return b.destroy.call(null,this),this}}),b.manifest={},b.registry=[],b.registryByName={},b.plugin=function(t,e,r){if(b.protect.natives.indexOf(t.toLowerCase())>=0)return void b.error("'"+t+"' is a protected function name");var a="function"==typeof e,s=["start","end","type","manifest"],d=["_setup","_teardown","start","end","frame"],u={},p=function(t,e){return t=t||b.nop,e=e||b.nop,function(){t.apply(this,arguments),e.apply(this,arguments)}};b.manifest[t]=r=r||e.manifest||{},d.forEach(function(n){e[n]=o(e[n]||b.nop,t)});var f=function(e,a){if(!a)return this;if(a.ranges&&b.isArray(a.ranges))return b.forEach(a.ranges,function(e){var n=b.extend({},a,e);delete n.ranges,this[t](n)},this),this;var i,o=a._natives={},u="";return b.extend(o,e),a._natives.type=a._natives.plugin=t,a._running=!1,o.start=o.start||o["in"],o.end=o.end||o.out,a.once&&(o.end=p(o.end,function(){this.removeTrackEvent(a._id)})),o._teardown=p(function(){var t=c.call(arguments),e=this.data.running[o.type];t.unshift(null),t[1]._running&&e.splice(e.indexOf(a),1)&&o.end.apply(this,t),t[1]._running=!1,this.emit("trackend",b.extend({},a,{plugin:o.type,type:"trackend",track:b.getTrackEvent(this,a.id||a._id)}))},o._teardown),o._teardown=p(o._teardown,function(){this.emit("trackteardown",b.extend({},a,{plugin:t,type:"trackteardown",track:b.getTrackEvent(this,a.id||a._id)}))}),a.compose=a.compose||[],"string"==typeof a.compose&&(a.compose=a.compose.split(" ")),a.effect=a.effect||[],"string"==typeof a.effect&&(a.effect=a.effect.split(" ")),a.compose=a.compose.concat(a.effect),a.compose.forEach(function(t){u=b.compositions[t]||{},d.forEach(function(t){o[t]=p(o[t],u[t])})}),a._natives.manifest=r,"start"in a||(a.start=a["in"]||0),a.end||0===a.end||(a.end=a.out||Number.MAX_VALUE),l.call(a,"toString")||(a.toString=function(){var e=["start: "+a.start,"end: "+a.end,"id: "+(a.id||a._id)];return null!=a.target&&e.push("target: "+a.target),t+" ( "+e.join(", ")+" )"}),a.target||(i="options"in r&&r.options,a.target=i&&"target"in i&&i.target),!a._id&&a._natives&&(a._id=b.guid(a._natives.type)),a instanceof n?(a._natives&&(a._id=a.id||a._id||b.guid(a._natives.type),a._natives._setup&&(a._natives._setup.call(this,a),this.emit("tracksetup",b.extend({},a,{plugin:a._natives.type,type:"tracksetup",track:a})))),this.data.trackEvents.add(a),n.start(this,a),this.timeUpdate(this,null,!0),a._id&&b.addTrackEvent.ref(this,a)):b.addTrackEvent(this,a),b.forEach(e,function(t,e){-1===s.indexOf(e)&&this.on(e,t)},this),this};b.p[t]=u[t]=function(r,o){var s,d,u,c,p;arguments.length;if(r&&!o)o=r,r=null;else{if(s=this.getTrackEvent(r))return p=o,c=i(s,p),s._natives._update?(this.data.trackEvents.remove(s),l.call(o,"start")&&(s.start=o.start),l.call(o,"end")&&(s.end=o.end),n.end(this,s),a&&e.call(this,s),s._natives._update.call(this,s,o),this.data.trackEvents.add(s),n.start(this,s),"cue"!==s._natives.type&&this.emit("trackchange",{id:s.id,type:"trackchange",previousValue:c,currentValue:p,track:s}),this):(b.extend(s,o),this.data.trackEvents.remove(r),s._natives._teardown&&s._natives._teardown.call(this,s),b.removeTrackEvent.ref(this,r),a?f.call(this,e.call(this,s),s):(s._id=s.id||s._id||b.guid(s._natives.type),s._natives&&s._natives._setup&&(s._natives._setup.call(this,s),this.emit("tracksetup",b.extend({},s,{plugin:s._natives.type,type:"tracksetup",track:s}))),this.data.trackEvents.add(s),n.start(this,s),this.timeUpdate(this,null,!0),b.addTrackEvent.ref(this,s)),this.emit("trackchange",{id:s.id,type:"trackchange",previousValue:c,currentValue:s,track:s}),this);o.id=r}return this.data.running[t]=this.data.running[t]||[],d=this.options.defaults&&this.options.defaults[t]||{},u=b.extend({},d,o),f.call(this,a?e.call(this,u):e,u),this},r&&b.extend(e,{manifest:r});var h={fn:u[t],definition:e,base:e,parents:[],name:t};return b.registry.push(b.extend(u,h,{type:t})),b.registryByName[t]=h,u},b.plugin.errors=[],b.plugin.debug="@VERSION"===b.version,b.removePlugin=function(t,e){if(!e){if(e=t,t=b.p,b.protect.natives.indexOf(e.toLowerCase())>=0)return void b.error("'"+e+"' is a protected function name");var n,r=b.registry.length;for(n=0;r>n;n++)if(b.registry[n].name===e)return b.registry.splice(n,1),delete b.registryByName[e],delete b.manifest[e],void delete t[e]}var a,i,o=t.data.trackEvents.byStart,s=t.data.trackEvents.byEnd,d=t.data.trackEvents.animating;for(a=0,i=o.length;i>a;a++)o[a]&&o[a]._natives&&o[a]._natives.type===e&&(o[a]._natives._teardown&&o[a]._natives._teardown.call(t,o[a]),o.splice(a,1),a--,i--,t.data.trackEvents.startIndex<=a&&(t.data.trackEvents.startIndex--,t.data.trackEvents.endIndex--)),s[a]&&s[a]._natives&&s[a]._natives.type===e&&s.splice(a,1);for(a=0,i=d.length;i>a;a++)d[a]&&d[a]._natives&&d[a]._natives.type===e&&(d.splice(a,1),a--,i--)},b.compositions={},b.compose=function(t,e,n){b.manifest[t]=n=n||e.manifest||{},b.compositions[t]=e},b.plugin.effect=b.effect=b.compose;var k=/^(?:\.|#|\[)/;b.dom={debug:!1,find:function(t,n){var r=null;if(n=n||e,t){if(!k.test(t)&&(r=e.getElementById(t),null!==r))return r;try{r=n.querySelector(t)}catch(a){if(b.dom.debug)throw new Error(a)}}return r}};var T=/\?/,w={ajax:null,url:"",data:"",dataType:"",success:b.nop,type:"GET",async:!0,contentType:"application/x-www-form-urlencoded; charset=UTF-8"};b.xhr=function(t){var e;return t.dataType=t.dataType&&t.dataType.toLowerCase()||null,!t.dataType||"jsonp"!==t.dataType&&"script"!==t.dataType?(e=b.extend({},w,t),e.ajax=new XMLHttpRequest,e.ajax?("GET"===e.type&&e.data&&(e.url+=(T.test(e.url)?"&":"?")+e.data,e.data=null),e.ajax.open(e.type,e.url,e.async),"POST"===e.type&&e.ajax.setRequestHeader("Content-Type",e.contentType),e.ajax.send(e.data||null),b.xhr.httpData(e)):void 0):void b.xhr.getJSONP(t.url,t.success,"script"===t.dataType)},b.xhr.httpData=function(t){var e,n,r=null,a=null;return t.ajax.onreadystatechange=function(){if(4===t.ajax.readyState){try{r=JSON.parse(t.ajax.responseText)}catch(i){}if(e={xml:t.ajax.responseXML,text:t.ajax.responseText,json:r},!e.xml||!e.xml.documentElement){e.xml=null;try{n=new DOMParser,a=n.parseFromString(t.ajax.responseText,"text/xml"),a.getElementsByTagName("parsererror").length||(e.xml=a)}catch(i){}}t.dataType&&(e=e[t.dataType]),t.success.call(t.ajax,e)}},e},b.xhr.getJSONP=function(t,n,r){var a,i,o,s=e.head||e.getElementsByTagName("head")[0]||e.documentElement,d=e.createElement("script"),u=!1,c=[],l=/(=)\?(?=&|$)|\?\?/;r||(o=t.match(/(callback=[^&]*)/),null!==o&&o.length?(a=o[1].split("=")[1],"?"===a&&(a="jsonp"),i=b.guid(a),t=t.replace(/(callback=[^&]*)/,"callback="+i)):(i=b.guid("jsonp"),l.test(t)&&(t=t.replace(l,"$1"+i)),c=t.split(/\?(.+)?/),t=c[0]+"?",c[1]&&(t+=c[1]+"&"),t+="callback="+i),window[i]=function(t){n&&n(t),u=!0}),d.addEventListener("load",function(){r&&n&&n(),u&&delete window[i],s.removeChild(d)},!1),d.addEventListener("error",function(t){n&&n({error:t}),r||delete window[i],s.removeChild(d)},!1),d.src=t,s.insertBefore(d,s.firstChild)},b.getJSONP=b.xhr.getJSONP,b.getScript=b.xhr.getScript=function(t,e){return b.xhr.getJSONP(t,e,!0)},b.util={toSeconds:function(t,e){var n,r,a,i,o,s,d=/^([0-9]+:){0,2}[0-9]+([.;][0-9]+)?$/,u="Invalid time format";return"number"==typeof t?t:("string"!=typeof t||d.test(t)||b.error(u),n=t.split(":"),r=n.length-1,a=n[r],a.indexOf(";")>-1&&(o=a.split(";"),s=0,e&&"number"==typeof e&&(s=parseFloat(o[1],10)/e),n[r]=parseInt(o[0],10)+s),i=n[0],{1:parseFloat(i,10),2:60*parseInt(i,10)+parseFloat(n[1],10),3:3600*parseInt(i,10)+60*parseInt(n[1],10)+parseFloat(n[2],10)}[n.length||1])}},b.p.cue=b.p.exec,b.protect={natives:E(b.p).map(function(t){return t.toLowerCase()})},b.forEach({listen:"on",unlisten:"off",trigger:"emit",exec:"cue"},function(t,e){var n=b.p[e];b.p[e]=function(){return"undefined"!=typeof console&&console.warn&&(console.warn("Deprecated method '"+e+"', "+(null==t?"do not use.":"use '"+t+"' instead.")),b.p[e]=n),b.p[t].apply(this,[].slice.call(arguments))}}),t.Popcorn=b}else{t.Popcorn={isSupported:!1};for(var x="byId forEach extend effects error guid sizeOf isArray nop position disable enable destroyaddTrackEvent removeTrackEvent getTrackEvents getTrackEvent getLastTrackEventId timeUpdate plugin removePlugin compose effect xhr getJSONP getScript".split(/\s+/);x.length;)t.Popcorn[x.shift()]=function(){}}}(window,window.document),function(t){var e=function(e,n){return e=e||t.nop,n=n||t.nop,function(){e.apply(this,arguments),n.apply(this,arguments)}};t.player=function(n,r){if(!t[n]){r=r||{};var a=function(n,a,i){i=i||{};var o,s,d=new Date/1e3,u=d,c=0,l=0,p=1,f=!1,h={},v="string"==typeof n?t.dom.find(n):n,y={};Object.prototype.__defineGetter__||(y=v||document.createElement("div"));for(var m in v)m in y||("object"==typeof v[m]?y[m]=v[m]:"function"==typeof v[m]?y[m]=function(t){return"length"in v[t]&&!v[t].call?v[t]:function(){return v[t].apply(v,arguments)}}(m):t.player.defineProperty(y,m,{get:function(t){return function(){return v[t]}}(m),set:t.nop,configurable:!0}));var g=function(){d=new Date/1e3,y.paused||(y.currentTime=y.currentTime+(d-u),y.dispatchEvent("timeupdate"),o=setTimeout(g,10)),u=d};return y.play=function(){this.paused=!1,y.readyState>=4&&(u=new Date/1e3,y.dispatchEvent("play"),g())},y.pause=function(){this.paused=!0,y.dispatchEvent("pause")},t.player.defineProperty(y,"currentTime",{get:function(){return c},set:function(t){return c=+t,y.dispatchEvent("timeupdate"),c},configurable:!0}),t.player.defineProperty(y,"volume",{get:function(){return p},set:function(t){return p=+t,y.dispatchEvent("volumechange"),p},configurable:!0}),t.player.defineProperty(y,"muted",{get:function(){return f},set:function(t){return f=+t,y.dispatchEvent("volumechange"),f},configurable:!0}),t.player.defineProperty(y,"readyState",{get:function(){return l},set:function(t){return l=t},configurable:!0}),y.addEventListener=function(t,e){return h[t]||(h[t]=[]),h[t].push(e),e},y.removeEventListener=function(t,e){var n,r=h[t];if(r){for(n=h[t].length-1;n>=0;n--)e===r[n]&&r.splice(n,1);return e}},y.dispatchEvent=function(e){var n,r,a=this,i=e.type;if(i||(i=e,r=t.events.getInterface(i),r&&(n=document.createEvent(r),n.initEvent(i,!0,!0,window,1))),h[i])for(var o=h[i].length-1;o>=0;o--)h[i][o].call(a,n,a)},y.src=a||"",y.duration=0,y.paused=!0,y.ended=0,i&&i.events&&t.forEach(i.events,function(t,e){y.addEventListener(e,t,!1)}),r._canPlayType(v.nodeName,a)!==!1?r._setup?r._setup.call(y,i):(y.readyState=4,y.dispatchEvent("loadedmetadata"),y.dispatchEvent("loadeddata"),y.dispatchEvent("canplaythrough")):setTimeout(function(){y.dispatchEvent("error")},0),s=new t.p.init(y,i),r._teardown&&(s.destroy=e(s.destroy,function(){r._teardown.call(y,i)})),s};a.canPlayType=r._canPlayType=r._canPlayType||t.nop,t[n]=t.player.registry[n]=a}},t.player.registry={},t.player.defineProperty=Object.defineProperty||function(e,n,r){
e.__defineGetter__(n,r.get||t.nop),e.__defineSetter__(n,r.set||t.nop)},t.player.playerQueue=function(){var t=[],e=!1;return{next:function(){e=!1,t.shift(),t[0]&&t[0]()},add:function(n){t.push(function(){e=!0,n&&n()}),!e&&t[0]()}}},t.smart=function(e,n,r){var a,i,o,s,d,u,c,l="string"==typeof e?t.dom.find(e):e,p="HTMLYouTubeVideoElement HTMLVimeoVideoElement HTMLSoundCloudAudioElement HTMLNullVideoElement".split(" ");if(!l)return void t.error("Specified target `"+e+"` was not found.");for(n="string"==typeof n?[n]:n,a=0,c=n.length;c>a;a++){for(i=n[a],o=0;o<p.length;o++)if(d=t[p[o]],d&&"probably"===d._canPlaySrc(i))return s=d(l),u=t(s,r),setTimeout(function(){s.src=i},0),u;for(var f in t.player.registry)if(t.player.registry.hasOwnProperty(f)&&t.player.registry[f].canPlayType(l.nodeName,i))return t[f](l,i,r)}var h,v,y=t.guid("popcorn-video-"),m=document.createElement("div");if(m.style.width="100%",m.style.height="100%",1===n.length)return v=document.createElement("video"),v.id=y,l.appendChild(v),setTimeout(function(){var t=document.createElement("div");t.innerHTML=n[0],v.src=t.firstChild.nodeValue},0),t("#"+y,r);for(l.appendChild(m),h='<video id="'+y+'" preload=auto autobuffer>',a=0,c=n.length;c>a;a++)h+='<source src="'+n[a]+'">';return h+="</video>",m.innerHTML=h,r&&r.events&&r.events.error&&l.addEventListener("error",r.events.error,!1),t("#"+y,r)}}(Popcorn),function(t,e){function n(t){for(var e=n.options,r=e.parser[e.strictMode?"strict":"loose"].exec(t),a={},i=14;i--;)a[e.key[i]]=r[i]||"";return a[e.q.name]={},a[e.key[12]].replace(e.q.parser,function(t,n,r){n&&(a[e.q.name][n]=r)}),a}function r(){var r,i={};return Object.prototype.__defineGetter__||(i=e.createElement("div")),i._util={type:"HTML5",TIMEUPDATE_MS:250,MIN_WIDTH:300,MIN_HEIGHT:150,isAttributeSet:function(t){return"string"==typeof t||t===!0},parseUri:n},i.addEventListener=function(t,n,r){e.addEventListener(this._eventNamespace+t,n,r)},i.removeEventListener=function(t,n,r){e.removeEventListener(this._eventNamespace+t,n,r)},i.dispatchEvent=function(t){var n=e.createEvent("CustomEvent"),r={type:t,target:this.parentNode,data:null};n.initCustomEvent(this._eventNamespace+t,!1,!1,r),e.dispatchEvent(n)},i.load=t.nop,i.canPlayType=function(t){return""},i.getBoundingClientRect=function(){return r.getBoundingClientRect()},i.NETWORK_EMPTY=0,i.NETWORK_IDLE=1,i.NETWORK_LOADING=2,i.NETWORK_NO_SOURCE=3,i.HAVE_NOTHING=0,i.HAVE_METADATA=1,i.HAVE_CURRENT_DATA=2,i.HAVE_FUTURE_DATA=3,i.HAVE_ENOUGH_DATA=4,Object.defineProperties(i,{currentSrc:{get:function(){return void 0!==this.src?this.src:""},configurable:!0},parentNode:{get:function(){return r},set:function(t){r=t},configurable:!0},preload:{get:function(){return"auto"},set:t.nop,configurable:!0},controls:{get:function(){return!0},set:t.nop,configurable:!0},poster:{get:function(){return""},set:t.nop,configurable:!0},crossorigin:{get:function(){return""},configurable:!0},played:{get:function(){return a},configurable:!0},seekable:{get:function(){return a},configurable:!0},buffered:{get:function(){return a},configurable:!0},defaultMuted:{get:function(){return!1},configurable:!0},defaultPlaybackRate:{get:function(){return 1},configurable:!0},style:{get:function(){return this.parentNode.style},configurable:!0},id:{get:function(){return this.parentNode.id},configurable:!0}}),i}n.options={strictMode:!1,key:["source","protocol","authority","userInfo","user","password","host","port","relative","path","directory","file","query","anchor"],q:{name:"queryKey",parser:/(?:^|&)([^&=]*)=?([^&]*)/g},parser:{strict:/^(?:([^:\/?#]+):)?(?:\/\/((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?))?((((?:[^?#\/]*\/)*)([^?#]*))(?:\?([^#]*))?(?:#(.*))?)/,loose:/^(?:(?![^:@]+:[^:@\/]*@)([^:\/?#.]+):)?(?:\/\/)?((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)/}};var a={length:0,start:t.nop,end:t.nop};window.MediaError=window.MediaError||function(){function t(t,e){this.code=t||null,this.message=e||""}return t.MEDIA_ERR_NONE_ACTIVE=0,t.MEDIA_ERR_ABORTED=1,t.MEDIA_ERR_NETWORK=2,t.MEDIA_ERR_DECODE=3,t.MEDIA_ERR_NONE_SUPPORTED=4,t}(),t._MediaElementProto=r}(Popcorn,window.document);