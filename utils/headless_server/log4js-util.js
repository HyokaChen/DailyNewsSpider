const log4js = require('log4js');
log4js.configure(
  {
    appenders: {
      file: {
        type: 'file',
        filename: './logs/chrome_server.log',
        maxLogSize: 10 * 1024 * 1024, // = 10Mb
        numBackups: 5, // keep five backup files
        compress: false, // compress the backups
        encoding: 'utf-8',
        mode: 0o0640,
        flags: 'w+'
      },
      dateFile: {
        type: 'dateFile',
        filename: './logs/chrome_server.log',
        pattern: 'yyyy-MM-dd-hh',
        compress: false
      },
      out: {
        type: 'stdout'
      }
    },
    categories: {
      default: { appenders: ['file', 'dateFile', 'out'], level: 'trace' }
    }
  }
);

const logger = log4js.getLogger('main');

module.exports = logger;