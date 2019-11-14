'use strict';

const express = require('express');
const bodyParser = require("body-parser");
const puppeteer = require('puppeteer-cn');
const request = require('request');
const debug = true;
const is_screenshot = true; // 默认开启截图
// const FdfsClient = require('fdfs');

//const fdfs_host = '127.0.0.1';
//const proxy_url = 'http://127.0.0.1:5000/get';
//const fdfs_port = 22122;
const app = express();
const proxy_url = undefined;

// var fdfs = new FdfsClient({
//     // tracker servers
//     trackers: [
//         {
//             host: fdfs_host,
//             port: fdfs_port
//         }
//     ],
//     // 默认超时时间10s
//     timeout: 10000,
//     // 默认后缀
//     // 当获取不到文件后缀时使用
//     defaultExt: 'png',
//     // charset默认utf8
//     charset: 'utf8'
// });

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));

app.post('/', function (req, res) {
    let url = req.body.url;
    console.log('url=>' + url);
    let operation = req.body.operation;
    console.log('operation=>' + operation);
    let cookiesStr = req.body.cookies;
    console.log('cookies=>' + cookiesStr);
    let result_type = req.body.result;
    console.log('result type=>' + result_type);

    let requestAction = function (url) {
        if (toString.call(url) !== '[object Undefined]' && url !== '')
            return undefined;
        return new Promise(function (resolve, reject) {
            request({
                url: url
            }, function (error, response, body) {
                if (error) return resolve('');
                resolve(body);
            })
        });
    };

    (async () => {
        let proxy = await requestAction(proxy_url);
        let browser;
        let headless_mode = true;
        if (debug === true) {
            headless_mode = false;
        }
        if (toString.call(proxy) !== '[object Undefined]' && proxy !== '') {
            console.log(0);
            browser = await puppeteer.launch({
                headless: headless_mode, // 关闭headless模式, 会打开浏览器
                ignoreHTTPSErrors: true, //如果是访问https页面 此属性会忽略https错误
                //设置超时时间
                timeout: 15000,
                args: ['--no-sandbox', '--disable-setuid-sandbox', '--proxy-server=' + proxy, '--start-maximized']
            });
            console.log('browser:' + proxy);
        } else {
            console.log(1);
            browser = await puppeteer.launch({
                headless: headless_mode,
                ignoreHTTPSErrors: true, //如果是访问https页面 此属性会忽略https错误
                //设置超时时间
                timeout: 15000,
                args: ['--no-sandbox', '--disable-setuid-sandbox', '--start-maximized']
            });
        }
        const pages = await browser.pages();
        let page = undefined;
        if (pages.length > 0)
            page = pages[0];
        else
            page = await browser.newPage();
        await page.setJavaScriptEnabled(true);
        const userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36';
        await page.setUserAgent(userAgent);
        if (toString.call(cookiesStr) !== '[object Undefined]' && cookiesStr !== '') {
            let cookiesObj = cookiesStr; //JSON.parse(cookiesStr);//转换为json对象
            for (let i = 0; i < cookiesObj.length; i++) {
                // let name = cookiesObj[i].name;  //取json中的值
                // let value = cookiesObj[i].value;
                await page.setCookie(cookiesObj[i]);
            }
        }
        await page.evaluateOnNewDocument(() => {
          Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
          });
        });
        await page.goto(url, {
            timeout: 180000
        }).then(() => {
            console.log('成功');
        }, () => {
            console.log('超时');
            browser.close();
            res.status(404).send(null);
        });

        await page.setViewport({
            width: 1366,
            height: 768
        });
        if (toString.call(operation) !== '[object Undefined]' && operation !== '') {
            // console.log(operation);
            for (let i = 0; i < operation.length; i++) {
                let operatorJson = operation[i];
                if (operatorJson.hasOwnProperty('scroll')) {
                    let sheight = operatorJson.scroll.height;
                    console.log(sheight);
                    await page.waitForNavigation({
                        waitUntil: 'domcontentloaded',
                        timeout: 60000
                    });
                    await page.evaluate(sheight => {
                        var total_height = document.body.scrollHeight;
                        if (Number(sheight) > total_height) {
                            console.log('scroll %%% 0 ~ ' + total_height);
                            window.scrollTo(0, total_height);
                        } else {
                            console.log('scroll %%% 0 ~ ' + sheight);
                            window.scrollTo(0, Number(sheight));
                        }
                    }, sheight).catch(err => {
                        console.log(err);
                        browser.close();
                        res.status(404).send(err.message);
                    });
                } else if (operatorJson.hasOwnProperty('window')) {
                    let inputValue = operatorJson.window.size;
                    let lengthArr = inputValue.split("x");
                    if (lengthArr.length === 2) {
                        let new_width = Number(lengthArr[0]);
                        let new_height = Number(lengthArr[1]);
                        console.log('reset window size %%% ' + inputValue);
                        await page.setViewport({
                            width: new_width,
                            height: new_height
                        }).catch(err => {
                            console.log(err);
                            browser.close();
                            res.status(404).send(err.message);
                        });
                    }
                } else {
                    let ele = undefined;
                    let inputValue = undefined;
                    let operatorName = undefined;
                    if (operatorJson.hasOwnProperty('input')) {
                        ele = operatorJson.input;
                        inputValue = ele.value;
                        operatorName = 'input';
                    } else if (operatorJson.hasOwnProperty('click')) {
                        ele = operatorJson.click;
                        operatorName = 'click';
                    }
                    let elementType = ele.type;
                    let elementValue = ele.dom;
                    if (elementType === 'css') {
                        await page.waitForSelector(elementValue, {
                            timeout: 60000,
                            visible: true
                        }).then(async () => {
                            if (operatorName === 'click') {
                                console.log(elementValue + ' %%%%% click!');
                                await page.evaluate(
                                    selector => {
                                        var node = document.querySelector(selector);
                                        node.click();
                                    }, elementValue);
                            } else if (operatorName === 'input') {
                                console.log(elementValue + ' %%%%% input!');
                                await page.focus(elementValue);
                                await page.type(elementValue, inputValue);
                            }
                        }).catch(err => {
                            console.log(err);
                            browser.close();
                            res.status(404).send(err.message);
                        });
                    } else if (elementType === 'xpath') {
                        await page.waitForXPath(elementValue, {
                            timeout: 60000,
                            visible: true
                        }).then(async () => {
                            let xpathElement = await page.$x(elementValue);
                            console.log(xpathElement);
                            if (operatorName === 'click') {
                                console.log(elementValue + ' %%%%% click!');
                                await page.evaluate(
                                    selector => {
                                        // var result = document.evaluate("//a[@href]", document, null, XPathResult.ANY_TYPE, null);
                                        // var nodes = result.iterateNext(); //枚举第一个元素
                                        // while (nodes) {
                                        //     // 对 nodes 执行操作;
                                        //     nodes = result.iterateNext(); //枚举下一个元素
                                        // }
                                        // 如果只查找单个元素，可以简写成这样
                                        var node = document.evaluate(selector, document).iterateNext();
                                        node.click();
                                    }
                                )
                                await xpathElement.click();
                            } else if (operatorName === 'input') {
                                console.log(elementValue + ' %%%%% input!');
                                await page.focus(elementValue);
                                await xpathElement.type(inputValue);
                            }
                        }).catch(err => {
                            console.log(err);
                            browser.close();
                            res.status(404).send(err.message);
                        });
                    }
                }
                let wait = operatorJson.wait;
                await page.waitFor(Number(wait));
            }
        }
        await page.waitFor(3000);
        if (is_screenshot === true) {
            await page.screenshot({
                path: './test.png',
                fullPage: true
            });
        }
        // let areaSelectStr = undefined;
        // // await page.waitForNavigation({
        // // 	waitUntil: 'load'
        // // });
        // // 页面渲染完毕后，开始截图
        // if (toString.call(areaSelectStr) !== '[object Undefined]' && areaSelectStr !== '') {
        //     let areaSelectJson = JSON.parse(areaSelectStr);
        //     let elementName = areaSelectJson['elementName'];
        //     let elementValue = areaSelectJson['elementValue'];
        //     console.log(elementValue);
        //     if (elementValue === '') {
        //         await page.screenshot({
        //             path: './test.png',
        //             fullPage: true
        //         });
        //     } else {
        //         let shotElement;
        //         if (elementName === 'css') {
        //             await page.waitForSelector(elementValue, {
        //                 timeout: 60000
        //             });
        //             shotElement = await page.$(elementValue);
        //         } else if (elementName === 'xpath') {
        //             await page.waitForXPath(elementValue, {
        //                 timeout: 60000
        //             });
        //             shotElement = await page.$x(elementValue);
        //         }
        //         await shotElement.screenshot({
        //             path: './test.png'
        //         });
        //     }

        //     // await fdfs.upload('./test.png').then(function (fileId) {
        //     //     let fileUrl = 'http://' + fdfs_host + '/' + fileId;
        //     //     res.set('_upUrl', fileUrl);
        //     //     console.log(fileUrl);
        //     // }).catch(function (err) {
        //     //     console.error(err);
        //     // })
        // }
        let result_str = result_type.split('&');
        let result = {}
        for (let j = 0; j < result_str.length; j++) {
            let return_type = result_str[j].trim();
            if (return_type === 'page') {
                let content = await page.content();
                result['result'] = content;
            } else if (return_type === 'cookies') {
                let cookies = await page.cookies();
                result['cookies'] = cookies;
            }
        }
        browser.close();
        res.status(200).send(result);
        console.log('send content ok~~~');
    })();
});

app.listen(5000, function () {
    console.log("Start server....5000")
});
