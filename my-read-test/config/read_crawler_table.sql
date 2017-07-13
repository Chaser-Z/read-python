create table `crawllist` (
	`id` int(20) not null AUTO_INCREMENT,
	`url` varchar(100) not null,
	`state` enum('1','0'),
	`info` varchar(100),
	`frequency` int(11) default '60',
	primary key(`id`)
)ENGINE=InnoDB default charset utf8;

create table `novelinfo`(
	`id` varchar(32) not null,
	`url` varchar(100) not null,
	`name` varchar(50),
	`author` varchar(30),
	`description` text,
	`type` varchar(20),
	`lastchapter` varchar(100),
	`chapterlisturl` varchar(100),
	`wordcount` int(11),
	`chaptercount` int(11),
	`keywords` varchar(100),
	`createtime` bigint(20),
	`updatetime` bigint(20),
	`state` enum('1','0'),
	
	primary key(`id`),
	index(`createtime`)
)ENGINE=InnoDB default charset utf8;

create table `novelchapter`(
	`id` varchar(32) not null,
	`novelid` varchar(32) not null,
	`url` varchar(100),
	`title` varchar(50),
	`wordcount` int(11),
	`chapterid` int(11),
	`chaptertime` bigint(20),
	`createtime` bigint(20),
	`state` enum('1','0'),
	
	primary key(`id`),
	index(`novelid`),
	index(`chapterid`),
	index(`chaptertime`)
)ENGINE=InnoDB default charset utf8;

create table `novelchapterdetail`(
	`id` varchar(32) not null,
	`url` varchar(100),
	`title` varchar(50),
	`wordcount` int(11),
	`chapterid` int(11),
	`chaptertime` bigint(20),
	`createtime` bigint(20),
	`content` text,
	`updatetime` bigint(20),
	
	primary key(`id`),
	index(`chaptertime`)
)ENGINE=InnoDB default charset utf8;