#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from pyspider.result import ResultWorker
from mymysql import SQL
import time
import logging
logger = logging.getLogger("result")


class MyResultWorker(ResultWorker):

    def on_result(self, task, result):

        logger.info('first line of on result')
        if not result or not result['title']:
            return

        logger.info('result not null')

        if 'taskid' in task and 'project' in task and 'url' in task:
            logger.info('result %s:%s %s -> %.30r' % (
        	task['project'], task['taskid'], task['url'], result))

	    result['taskid'] = task['taskid']
	    result['updatetime'] = time.time()
	    sql = SQL()
            logger.info('sql initiated')
	    sql.replace('crawl_table', **result)
            logger.info('result insert')

	else:
            logger.warning('result UNKNOW -> %.30r' % result)
            return
