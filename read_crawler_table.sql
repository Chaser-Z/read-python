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
  id int not null auto_increment,	
  article_id varchar(50),	
  title varchar(100),
  author varchar(50),
  article_abstract text,
  link varchar(500),
  image_link varchar(500),
  status int not null default 0,
  primary key(id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

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

