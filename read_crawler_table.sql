
create table c_article_list
(
  id int not null auto_increment,	 -- 主键id
  article_id varchar(50),			 -- 文章id
  title varchar(100),				 -- 文章标题
  author varchar(50),				 -- 作者
  article_abstract text,			 -- 文章摘要	
  link varchar(500),				 -- 文章链接	
  image_link varchar(500),			 -- 图片链接 
  article_type varchar(50),          -- 小说类型
  status int not null default 0,	 -- 状态	    0 - 默认  1 - 已经抓取，但是没有完结  2 - 完结，不用继续抓取
  primary key(id)					 -- 设置id为主键
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


create table c_article_detail
(
    id int not null auto_increment,	     -- 主键id  -- 自增长
    article_id varchar(50),	             -- 文章id
	title varchar(100),      			 -- 文章标题
	image_link varchar(500),			 -- 图片链接 	
	author varchar(50),					 -- 作者
	update_status varchar(10), 			 -- 更新或者完结状态
	last_update_date varchar(50),		 -- 最后更新时间
	last_update_directory varchar (50),	 -- 最后更新章节
	article_directory varchar(50),		 -- 章节名称
	article_directory_link varchar(50),	 -- 章节链接	
	content text,						 -- 内容 
	status int not null default 0,       -- 状态 0: default; 1: processed; 3: crawled
	primary key(id)						 -- 设置id为主键	
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

