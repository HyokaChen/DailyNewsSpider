const Redis = require('ioredis');
let redis = new Redis("redis://172.0.0.1:6379/3");
module.exports = redis;