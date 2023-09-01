function makeMulti (string) {
    let l = new String(string)
    l = l.substring(l.indexOf("/*") + 3, l.lastIndexOf("*/"))
    return "%c " + l
}
let string = function () {
/*
           _____       _     __          ____
          / ___/____  (_)___/ /__  _____/ __ )____  _  __     爬虫爬得欢
          \__ \/ __ \/ / __  / _ \/ ___/ __  / __ \| |/_/     监狱要坐穿
         ___/ / /_/ / / /_/ /  __/ /  / /_/ / /_/ />  <       数据玩得溜
        /____/ .___/_/\__,_/\___/_/  /_____/\____/_/|_|       牢饭吃个够
            /_/
*/
}
console.log(makeMulti(string), "color: #0084ff");
console.log("\n %c © BOB'S BLOG %c itbob.cn %c © SpiderBox %c spiderbox.cn %c © WebStack %c webstack.cc \n", "color: #fadfa3; background: #030307; padding:5px 0;", "background: #fadfa3; padding:5px 0;", "color: #ffffff; background: #0084ff; padding:5px 0;", "background: #fadfa3; padding:5px 0;", "color: #ffffff; background: #f1404b; padding:5px 0;", "background: #fadfa3; padding:5px 0;")
