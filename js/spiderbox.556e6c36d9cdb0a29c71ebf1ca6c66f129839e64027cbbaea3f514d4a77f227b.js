/* 控制台输出 */
function makeMulti(string) {
    let l = new String(string)
    l = l.substring(l.indexOf("/*") + 3, l.lastIndexOf("*/"))
    return "%c " + l
};
const string = function () {
    /*
          _____       _     __          ____
         / ___/____  (_)___/ /__  _____/ __ )____  _  __         爬虫爬得欢
         \__ \/ __ \/ / __  / _ \/ ___/ __  / __ \| |/_/        监狱要坐穿
        ___/ / /_/ / / /_/ /  __/ /  / /_/ / /_/ />  <         数据玩得溜
       /____/ .___/_/\__,_/\___/_/  /_____/\____/_/|_|        牢饭吃个够
           /_/
    */
};
console.log(makeMulti(string), "color: #0084ff");
console.log("\n %c © BOB'S BLOG %c itbob.cn %c © SpiderBox %c spiderbox.cn %c © WebStack %c webstack.cc \n", "color: #fadfa3; background: #030307; padding:5px 0;", "background: #fadfa3; padding:5px 0;", "color: #ffffff; background: #0084ff; padding:5px 0;", "background: #fadfa3; padding:5px 0;", "color: #ffffff; background: #f1404b; padding:5px 0;", "background: #fadfa3; padding:5px 0;");

/* 弹窗一：say hello baby */
$(document).ready(function () {
    // 检查本地存储中的标志位，如果标志位为 true，则不再弹出弹窗
    let lastPopupTime = localStorage.getItem("FUCK_GIZAWORKS");
    lastPopupTime = new Date(lastPopupTime).getTime();
    const currentTime = new Date().getTime();
    const timeDifferenceInDays = Math.floor((currentTime - lastPopupTime) / (1000 * 60 * 60 * 24));
    if (!lastPopupTime || timeDifferenceInDays >= 10) {
        Swal.fire({
            // width: 300,
            title: "欢迎",
            // text: "SpiderBox 仍处于初期建设当中，<br>欢迎扫码关注站长公众号：虫技",
            html: `
            <!-- <font style="font-weight:bold; color:red;">SpiderBox 仍处于初期建设当中</font>-->
            <!-- <br>-->
            欢迎扫码关注站长公众号：虫技
            <br>
            <p style="color:#DC1729;"><strong>本站与 kgtools.cn 等其他网站没有任何关系</strong></p>
            <p style="color:#DC1729;"><strong>本站于2023年8月13日原创首发，<a href="https://mp.weixin.qq.com/s/7vFpmhvU8-DCONlvlklMTQ" target="_blank">点此了解详情</a></strong></p>
            <p style="color:#DC1729;"><strong>本站不定期就会遭遇攻击，可能会出现无法访问的情况。</strong></p>            
            `,
            showCancelButton: true,
            confirmButtonText: "俺知道了",
            cancelButtonText: "烦死了，近期不再弹出！",
            confirmButtonColor: "#0084ff",
            imageUrl: "https://static.spiderapi.cn/spiderbox/images/qrcode/IT_BOB.jpg",
            // imageUrl: "https://spiderapi.cn/img/qrcode/gzh.png",
            // imageWidth: 300,
            // imageHeight: 300,
            imageAlt: "公众号：虫技",
            showClass: {
                popup: "swal2-show"
            },
            hideClass: {
                popup: "swal2-hide"
            }
        }).then((result) => {
            if (result.isConfirmed) {

            } else {
                localStorage.setItem("FUCK_GIZAWORKS", new Date().toISOString());
            }
        });
        const popupContainer = document.querySelector('.swal2-container');
        popupContainer.style.zIndex = '9999';
    }
});

/* 弹窗二：交流群 */
$(document).ready(function () {
    const showGroupElement = document.getElementById("show-group");
    showGroupElement.addEventListener("click", function () {
        Swal.fire({
            text: "扫码加入QQ / 微信交流群",
            confirmButtonText: "俺知道了",
            confirmButtonColor: "#0084ff",
            imageWidth: 420,
            imageUrl: "https://static.spiderapi.cn/spiderbox/images/group.webp",
            imageAlt: "QQ / 微信交流群",
            showClass: {
                popup: "swal2-show"
            },
            hideClass: {
                popup: "swal2-hide"
            },
            allowOutsideClick: false,
            customClass: {
                image: "custom-swal-image"
            }
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.close();
            }
        });
        const popupContainer = document.querySelector(".swal2-container");
        popupContainer.style.zIndex = "9999";
    })
});

/* 弹窗三：免责声明 */
$(document).ready(function () {
    let popupWidth = "55%"; // 默认宽度
    if (window.innerWidth < 768) {
        popupWidth = "95%";
    } else {
        popupWidth = "55%";
    }

    const showDisclaimerElement = document.getElementById("show-disclaimer");
    showDisclaimerElement.addEventListener("click", function () {
        Swal.fire({
            html: `
            <div class="custom-swal-container">
                <h3>免责声明</h3>
                <p style="text-align: left;">欢迎使用我们的导航站 [SpiderBox 虫盒]！请在使用本站点之前仔细阅读以下免责声明，要访问和使用本站点，您必须接受以下条款和条件！如果您不同意这些条款和条件，请勿使用本站点！</p>
                <ol class="custom-swal-ol">
                    <li>
                        <span>信息准确性</span>
                        <p>本站点提供的导航链接和信息仅供参考，尽管我们努力确保信息的准确性和完整性，但我们不对信息的准确性、完整性、实时性或适用性作出任何明示或暗示的陈述或担保，您应该自行核实和验证您所获得的信息！</p>
                    </li>
                    <li>
                        <span>使用风险</span>
                        <p>使用本站点提供的导航链接和信息是基于您自己的判断和风险，我们不对您使用本站点导航链接导致的任何损失、损害或不便负责，在使用导航链接之前，请确保您已经充分了解所涉及的风险！</p>
                    </li>
                    <li>
                        <span>第三方链接</span>
                        <p>本站点包含的所有指向第三方网站的链接仅供您的方便提供，不代表我们对这些第三方网站的认可或担保，我们对这些第三方网站的内容、隐私政策和行为不承担任何责任，您在访问这些链接时需谨慎自负风险！</p>
                    </li>
                    <li>
                        <span>知识产权和版权</span>
                        <p>本站点为非营利性网站，尊重知识产权和版权，基于互联网之分享精神，如果您认为本站点包含侵犯您的知识产权或版权的内容，请与我们联系，我们会尽快删除或更正相关内容！</p>
                    </li>
                    <li>
                        <span>法律合规</span>
                        <p>您使用本站点的行为应遵守适用的法律法规，您对任何违反法律法规的行为负有全部责任，我们不对您的任何违法行为负责！</p>
                    </li>
                    <li>
                        <span>免责声明的变更</span>
                        <p>我们保留随时修改或更新本免责声明的权利，请您定期查阅本页面以获取最新信息！</p>
                    </li>
                  </ol>
    
                  <h3>联系方式</h3>
                  <ol class="custom-swal-ol">
                    <li>
                        <span>站长邮箱：</span>
                        <button style="display: inline;margin: 0;" id="show-email">点击获取</button>
                    </li>
                    <li>
                        <span>站长公众号：</span>虫技
                    </li>
                  </ol>
                  <p class="custom-swal-date">2023年08月17日</p>
            </div>
            `,
            width: popupWidth,
            showCancelButton: true,
            confirmButtonText: "同意",
            cancelButtonText: "不同意",
            confirmButtonColor: "#0084ff",
            showClass: {
                popup: "swal2-show"
            },
            hideClass: {
                popup: "swal2-hide"
            },
            allowOutsideClick: false,
            customClass: {
                // popup: "custom-swal-popup"
                container: "custom-swal-container"
            }
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.close();
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                window.close();
            }
        });
        const popupContainer = document.querySelector(".swal2-container");
        popupContainer.style.zIndex = "9999";

        let showEmailElement = document.getElementById("show-email");
        showEmailElement.addEventListener("click", function () {
            showEmailElement.innerHTML = atob("YWRtaW5AaXRib2IuY24=");
        });
    });
});

/* 弹窗四：打赏赞助 */
// $(document).ready(function () {
//     const showSponsorElement = document.getElementById("show-sponsor");
//     showSponsorElement.addEventListener("click", function () {
//         Swal.fire({
//             text: "所有打赏、赞助将用于 SpiderBox 的域名、服务器、COS 等项目续费。",
//             confirmButtonText: "俺知道了",
//             confirmButtonColor: "#0084ff",
//             imageWidth: 420,
//             imageUrl: "https://static.spiderapi.cn/spiderbox/images/sponsor.webp",
//             imageAlt: "微信 / 支付宝收款码",
//             showClass: {
//                 popup: "swal2-show"
//             },
//             hideClass: {
//                 popup: "swal2-hide"
//             },
//             allowOutsideClick: false,
//             customClass: {
//                 image: "custom-swal-image"
//             }
//         }).then((result) => {
//             if (result.isConfirmed) {
//                 Swal.close();
//             }
//         });

//         const popupContainer = document.querySelector(".swal2-container");
//         popupContainer.style.zIndex = "9999";
//     })
// });

/* 夜间(日间)模式 */
(function () {
    if (document.cookie.replace(/(?:(?:^|.*;\s*)night\s*\=\s*([^;]*).*$)|^.*$/, "$1") === '') {
        if (new Date().getHours() > 22 || new Date().getHours() < 6) {
            document.body.classList.remove('io-black-mode');
            document.body.classList.add('io-grey-mode');
            document.cookie = "night=1;path=/";
            console.log('夜间模式开启');
        } else {
            document.body.classList.remove('night');
            document.cookie = "night=0;path=/";
            console.log('夜间模式关闭');
        }
    } else {
        let night = document.cookie.replace(/(?:(?:^|.*;\s*)night\s*\=\s*([^;]*).*$)|^.*$/, "$1") || '0';
        if (night == '0') {
            document.body.classList.remove('night');
        } else if (night == '1') {
            document.body.classList.add('night');
        }
    }
})();

/* 夜间(日间)模式切换 */
// $("#search-bg").css("background-image", "url({{ with $.Site.Params.cdnURL }}{{ . }}{{ end }}{{ $.Site.Params.images.searchImageL }})");   //默认浅色背景
function switchNightMode() {
    let night = document.cookie.replace(/(?:(?:^|.*;\s*)night\s*\=\s*([^;]*).*$)|^.*$/, "$1") || '0';
    if (night == '0') {
        // $("#search-bg").css("background-image", "url({{ with $.Site.Params.cdnURL }}{{ . }}{{ end }}{{ $.Site.Params.images.searchImageL }})");
        document.body.classList.remove('io-grey-mode');
        document.body.classList.add('io-black-mode');
        document.cookie = "night=1;path=/"
        console.log(' ');
        $(".switch-dark-mode").attr("data-original-title", "日间模式");
        $(".mode-ico").removeClass("icon-night");
        $(".mode-ico").addClass("icon-light");
    } else {
        // $("#search-bg").css("background-image", "url({{ with $.Site.Params.cdnURL }}{{ . }}{{ end }}{{ $.Site.Params.images.searchImageD }})")
        document.body.classList.remove('io-black-mode');
        document.body.classList.add('io-grey-mode');
        document.cookie = "night=0;path=/"
        console.log(' ');
        $(".switch-dark-mode").attr("data-original-title", "夜间模式");
        $(".mode-ico").removeClass("icon-light");
        $(".mode-ico").addClass("icon-night");
    }
}

/* 图片懒加载 */
$(document).ready(function () {
    let observer = new IntersectionObserver((entries, observe) => {
        entries.forEach(item => {
            // 获取当前正在观察的元素
            let target = item.target
            if (item.isIntersecting && target.dataset.src) {
                target.src = target.dataset.src
                // 删除data-src属性
                target.removeAttribute("data-src")
                // 取消观察
                observe.unobserve(item.target)
            }
        })
    })
    //   let allLazyImgs = document.querySelectorAll(".lazy")
    //   allLazyImgs.forEach(item => {
    //       // 遍历观察元素
    //       observer.observe(item)
    //   })
    let allLazyImgs = document.querySelectorAll(".lazy")
    let isScrolling = false;

    window.addEventListener('scroll', function () {
        if (!isScrolling) {
            window.requestAnimationFrame(function () {
                allLazyImgs.forEach(item => {
                    if (isElementInViewport(item) && item.dataset.src) {
                        observer.observe(item);
                    }
                });
                isScrolling = false;
            });
        }
        isScrolling = true;
    });

    function isElementInViewport(el) {
        let rect = el.getBoundingClientRect();
        return (
            rect.bottom >= 0 &&
            rect.right >= 0 &&
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.left <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    allLazyImgs.forEach(item => {
        if (isElementInViewport(item) && item.dataset.src) {
            observer.observe(item);
        }
    });
});

