需要把这两个文件放在Pyspider的根目录下。

在默认的result_worker中，传入replace方法的dict 结构大概是：

	{
		prroject:task[project],
		taskid:task[taskid],
		url:task[url],
		result:result
		
	}

其中，task和result变量 都是回调函数on_result的参数，这里重写on_result函数：

	    result['taskid'] = task['taskid']
	    result['updatetime'] = time.time()
	    sql = SQL()
            logger.info('sql initiated')
	    sql.replace('crawl_table', **result)
            logger.info('result insert')

这里的dict就会变成result定义的dict,每一项都是爬虫爬下来的一个item信息，和数据库中对应表结构相同，因此直接传给自己定义的sql处理replace函数就可以实现pyghon dict到mysql 表的对应insert。