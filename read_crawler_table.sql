create table c_article_list
(
	cover_link varchar(500),
	topic varchar(100),
	title varchar(50),
	source varchar(200),
	push_date varchar(50),
	digest text,
    article_id varchar(50), -- unique
    article_link varchar(500),
    raw_text text,
	status int not null default 0 -- 0: default; 1: processed; 3: crawled
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table c_article_hot_list
(
  id int not null auto_increment,	 -- 主键id
  article_id varchar(50),			 -- 文章id
  title varchar(100),				 -- 文章标题
  author varchar(50),				 -- 作者
  article_abstract text,			 -- 文章摘要	
  link varchar(500),				 -- 文章链接	
  image_link varchar(500),			 -- 图片链接 
  status int not null default 0,	 -- 状态	
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
	airicle_directory varchar(50),		 -- 章节名称
	article_directory_link varchar(50),	 -- 章节链接	
	content text,						 -- 内容 
	status int not null default 0,       -- 状态 0: default; 1: processed; 3: crawled
	primary key(id)						 -- 设置id为主键	
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table c_article_update_info
(
title varchar(100),
update_status varchar(10), -- 更新或者完结
last_update_date varchar(50),
last_update_directory varchar (50)
)ENGINE=MyISAM DEFAULT CHARSET=utf8;
create table c_article_directory_list
(
	airicle_directory varchar(50),
	article_directory_link varchar(50),
	status int not null default 0
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table c_article_content
(
	title varchar(50),
	content text,
	status int not null default 0
	
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

