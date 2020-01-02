'use strict';

const express = require('express');
const bodyParser = require("body-parser");
const pageZbject = require('./puppeteer_object.js');
const is_screenshot = true; // 默认开启截图
const app = express();
const page_object = new pageZbject();
const error_msg = {
    "status": "Error",
    "msg": ""
};
const ok_msg = {
    "status": "Ok",
    "msg": "",
    "data": ""
};
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));

app.post('/', function (req, res) {
    let url = req.body.url;
    let incognito = req.body.incognito;
    let check = req.body.check;
    console.log('url=>' + url);
    (async () => {
        await page_object.init(incognito);
        const page = page_object.page;
        if (url != null && !page_object.attach) {
            await page.goto(url, {
                timeout: 120000
            }).then(() => {
                console.log('成功');
            }, () => {
                console.log('超时');
                error_msg.msg = `请求=>${url} 超时`;
                res.status(404).send(error_msg);
            });
            await page.setJavaScriptEnabled(true);
            // const userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36';
            // await page.setUserAgent(userAgent);
            await page.setViewport({
                width: 1000,
                height: 600
            });
            let cookies = await page.cookies();
            console.log(cookies);
            if (toString.call(check) !== '[object Undefined]' && check !== '') {
                await page.waitForSelector(check, {timeout: 10000}).then(
                    async () => {
                        let dom = await page.$(check);
                        if (dom == null) {
                            ok_msg.msg = "不需要登录";
                        } else {
                            ok_msg.msg = "需要登录";
                        }
                    }
                ).catch(err => {
                    console.log(err);
                    ok_msg.msg = "不需要登录";
                });

            } else {
                ok_msg.msg = `请求=> ${url} 成功`;
            }
            res.status(200).send(ok_msg);
        }
        res.status(200).send(ok_msg);
    })();
});
app.post('/refresh', function (req, res) {
    let url = req.body.url;
    console.log('url=>' + url);
    (async () => {
        const page = page_object.page;
        if (url != null) {
            await page.goto(url, {
                timeout: 120000
            }).then(() => {
                console.log('成功');
            }, () => {
                console.log('超时');
                error_msg.msg = `重试=>${url} 超时`;
                res.status(404).send(error_msg);
            });
            ok_msg.msg = `重试=> ${url} 成功`;
            res.status(200).send(ok_msg);
        }
        res.status(200).send(ok_msg);
    })();
});
app.get('/close', function (req, res) {
    (async () => {
        await page_object.close();
        ok_msg.msg = "关闭浏览器成功";
        res.status(200).send(ok_msg);
    })();
});
app.post('/work', function (req, res) {
    let operation = req.body.operation;
    console.log(`operation=> ${operation}`);
    // let cookiesStr = req.body.cookies;
    // console.log('cookies=>' + cookiesStr);
    let result_type = req.body.result;
    console.log(`result type=>${result_type}`);
    (async () => {
        const page = page_object.page;
        if (toString.call(operation) !== '[object Undefined]' && operation !== '') {
            console.log(JSON.stringify(operation));
            for (let i = 0; i < operation.length; i++) {
                let operatorJson = operation[i];
                let ele = undefined;
                let inputValue = undefined;
                let operatorName = undefined;
                let waitLoad = false;
                let file = false;
                if (operatorJson.hasOwnProperty('input')) {
                    ele = operatorJson.input;
                    inputValue = ele.value;
                    operatorName = 'input';
                } else if (operatorJson.hasOwnProperty('click')) {
                    ele = operatorJson.click;
                    operatorName = 'click';
                    waitLoad = ele.hasOwnProperty('wait_load') ? ele.wait_load : waitLoad;
                    file = ele.hasOwnProperty('file') ? ele.file : file;
                } else if (operatorJson.hasOwnProperty('select')) {
                    ele = operatorJson.select;
                    operatorName = 'select';
                    inputValue = ele.value;
                } else if (operatorJson.hasOwnProperty('upload')) {
                    ele = operatorJson.upload;
                    operatorName = 'upload';
                    inputValue = ele.path;
                } else if (operatorJson.hasOwnProperty("check")) {
                    ele = operatorJson.check;
                    operatorName = 'check';
                    inputValue = ele.condition;
                }
                if (toString.call(ele) === '[object Undefined]') {
                    error_msg.msg = "暂不支持除[input, click, select, upload, check]外方法";
                    res.status(404).send(error_msg);
                }
                let frame = undefined;
                try {
                    frame = page.mainFrame();
                } catch (e) {
                    frame = page;
                }
                if (ele.hasOwnProperty('frame')) {
                    console.log(ele.frame);
                    console.log("----------------frame----------------");
                    // page.mainFrame().childFrames().forEach(f => console.log(f.name()));
                    frame = await page.mainFrame().childFrames().find(f => f.name() === ele.frame);
                }
                let elementType = ele.type;
                let elementValue = ele.dom;
                if (elementType === 'css') {
                    console.log(`element>>>${elementValue}`);
                    if (operatorName === 'check') {
                        await frame.waitForSelector(elementValue, {timeout: 5000})
                            .then(async () => {
                                if (inputValue === false) {
                                    console.log("condition not fill");
                                    error_msg.msg = "条件未满足";
                                    res.status(404).send(error_msg);
                                } else {
                                    console.log("找到--");
                                    console.log("condition fill");
                                }
                            }).catch(() => {
                                if (inputValue === true) {
                                    console.log("condition not fill");
                                    error_msg.msg = "条件未满足";
                                    res.status(404).send(error_msg);
                                } else {
                                    console.log("未找到--");
                                    console.log("condition fill");
                                }
                            });
                        continue;
                    }
                    await frame.waitForSelector(elementValue, {
                        timeout: 20000
                    }).then(async () => {
                        if (operatorName === 'click') {
                            console.log(`${elementValue} %%%%% click!`);
                            console.log(`${frame.name()} %%%%% iframe`);
                            const node_disable = await frame.evaluate(
                                selector => {
                                    let node = document.querySelector(selector);
                                    console.log(node.name);
                                    if (!node.hasAttribute("disabled")) {
                                        console.log("点击" + selector);
                                        node.click();
                                        return true;
                                    }
                                    return false;
                                }, elementValue);
                            await page.bringToFront();
                            if (node_disable && (waitLoad || file)) {
                                await page.waitForResponse(resp => resp.ok());
                            }
                            if (file) {
                                ok_msg.data = "等待下载完成";
                            }
                        } else if (operatorName === 'input') {
                            console.log(`${elementValue} %%%%% input!`);
                            await frame.focus(elementValue);
                            await frame.evaluate(
                                (selector, value) => {
                                    let node = document.querySelector(selector);
                                    console.log(node.name);
                                    node.value = "";
                                    node.value = value;
                                }, elementValue, inputValue);
                            // await frame.type(elementValue, "");
                            // await frame.type(elementValue, inputValue);
                        } else if (operatorName === 'select') {
                            console.log(`${elementValue} %%%%% select!`);
                            await frame.select(elementValue, ...inputValue);
                        } else if (operatorName === 'upload') {
                            console.log(`${elementValue} %%%%% upload!`);
                            let upload_file = await frame.$(elementValue);
                            await upload_file.uploadFile(inputValue);
                        }
                    }).catch(err => {
                        console.log(err);
                        error_msg.msg = err.message;
                        res.status(404).send(error_msg);
                    });
                }
                let wait = operatorJson.wait;
                if (toString.call(wait) === '[object Undefined]') {
                    wait = 300;
                }
                await page.waitFor(Number(wait));
            }
        }
        await page.waitFor(5000);
        if (is_screenshot === true) {
            await page.screenshot({
                path: './work.png',
                fullPage: true
            });
        }
        let result = {"result": "ok"};
        if (toString.call(result_type) !== '[object Undefined]' && result_type !== '') {
            console.log("返回数据");
            let result_str = result_type.split('&');
            for (let j = 0; j < result_str.length; j++) {
                let return_type = result_str[j].trim();
                if (return_type === 'page') {
                    result['result'] = await page.content();
                } else if (return_type === 'cookies') {
                    let uu = await page.url();
                    console.log(uu);
                    //await page._client.send('Network.getAllCookies');
                    let cookies = await page.cookies();
                    console.log(cookies);
                    result['cookies'] = cookies;
                }
            }
        }
        ok_msg.msg = "执行work成功";
        res.status(200).send(ok_msg);
        console.log('send content ok~~~');
    })();
});


app.listen(8001, function () {
    console.log("Start server....")
});