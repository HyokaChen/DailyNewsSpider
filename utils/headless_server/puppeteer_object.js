'use strict';

const puppeteer = require('puppeteer');
const axios = require('axios');
const debug = true;
class PageObject{
     constructor(){
        this.browser = null;
        this.page = null;
        this.incognito = true;
        this.attach = false;
     }
     async get_debug_url() {
         // 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe' --remote-debugging-port=9222 --user-data-dir="C:\iRobot\user"
         let res = await axios.get("http://localhost:9222/json/version");
         return res.data.webSocketDebuggerUrl;
     }
     async init(incognito){
        let headless_mode = true;
        if (debug === true) {
            headless_mode = false;
        }
        this.incognito = incognito;
        // 重复利用
        if (this.browser == null) {
            console.log(1);
            try {
                let ws = await this.get_debug_url();
                this.browser = await  puppeteer.connect({
                    browserWSEndpoint: ws,
                    defaultViewport: null
                });
                this.attach = true;
            }
            catch(err){
                console.log("")
                if (this.incognito === true) {
                    this.browser = await puppeteer.launch({
                        ignoreDefaultArgs: true,
                        headless: headless_mode,
                        executablePath: '/Applications/"Microsoft Edge Beta.app"/Contents/MacOS/"Microsoft Edge Beta',
                        ignoreHTTPSErrors: false, //如果是访问https页面 此属性会忽略https错误
                        //设置超时时间
                        timeout: 15000,
                        args: ['--disable-dev-shm-usage',
                            '--incognito',
                            '--start-maximized']
                    });
                } else {
                    this.browser = await puppeteer.launch({
                        ignoreDefaultArgs: true,
                        headless: headless_mode,
                        executablePath: '/Applications/"Microsoft Edge Beta.app"/Contents/MacOS/"Microsoft Edge Beta"',
                        ignoreHTTPSErrors: false, //如果是访问https页面 此属性会忽略https错误
                        //设置超时时间
                        timeout: 15000,
                        args: ['--disable-dev-shm-usage',
                            '--start-maximized']
                    });
                }
            }

        }
        const pages = await this.browser.pages();
        if (pages.length > 0)
            this.page = pages[0];
        else
            this.page = await this.browser.newPage();
     }

     async close(){
         if (this.browser != null){
             await this.browser.close();
             this.browser = null;
         }
     }
}
module.exports = PageObject;