#!/usr/bin/env python
from collections import namedtuple

#######################################  规则  ###########################################
# DOMAIN
# 不可用的域名
BLACK_DOMAIN = ['www.17k.com', 'mm.17k.com', 'www.xs8.cn', 'www.zongheng.com', 'yunqi.qq.com', 'chuangshi.qq.com',
                'book.qidian.com', 'www.soduso.com', 'pages.book.qq.com', 'book.km.com', 'www.lread.net',
                'www.0dsw.com', 'www.5200xsb.com', 'www.80txt.com', 'www.sodu.tw', 'www.shuquge.com',
                'www.shenmanhua.com', 'xiaoshuo.sogou.com', 'www.999wx.com', 'zetianji8.com', 'www.bookso.net',
                'm.23us.com', 'www.qbxsw.com', 'www.zhuzhudao.com', 'www.shengyan.org', 'www.360doc.com',
                'www.ishuo.cn', 'read.qidian.com', 'www.yunlaige.com', 'www.qidian.com', 'www.sodu888.com',
                'www.siluke.cc', 'read.10086.cn', 'www.pbtxt.com', 'c4txt.com', 'www.bokon.net', 'www.sikushu.net',
                'www.is028.cn', 'www.tadu.com', 'www.kudu8.com', 'www.bmwen.com', 'www.5858xs.com', 'www.yiwan.com',
                'www.x81zw.com', 'www.123du.cc', 'www.chashu.cc', '20xs.com', 'www.haxwx.net', 'www.dushiwenxue.com',
                "www.yxdown.com", 'www.jingcaiyuedu.com', 'www.zhetian.org', 'www.xiaoshuo02.com', 'www.xiaoshuo77.com',
                'www.868xh.com', 'dp.changyou.com', 'www.iyouman.com', 'www.qq717.com', 'www.yznn.com', "www.69w.cc",
                "www.doupocangqiong1.com", "www.manhuatai.com", "www.5wxs.com", "www.ggshuji.com", "www.msxf.net",
                "www.mianhuatang.la", "www.boluoxs.com", "www.lbiquge.top", "www.69shu.com", "www.qingkan520.com",
                "book.douban.com", "movie.douban.com", "www.txshuku.com", "lz.book.sohu.com", "www.3gsc.com.cn",
                "www.txtshu365.com", "www.517yuedu.com", "www.baike.com", "read.jd.com", "www.zhihu.com", "wshuyi.com",
                "www.19lou.tw", "www.chenwangbook.com", "www.aqtxt.com", "book.114la.com", "www.niepo.net",
                "me.qidian.com", "www.gengd.com", "www.77l.com", "www.geilwx.com", "www.97xiao.com", "www.anqu.com",
                "www.wuxiaxs.com", "yuedu.163.com", "b.faloo.com", "bbs.qidian.com", "jingji.qidian.com", "www.sodu.cc",
                "forum.qdmm.com", "www.qdmm.com", "game.91.com", "www.11773.com", "mt.sohu.com", "book.dajianet.com",
                "haokan.17k.com", "www.qmdsj.com", "www.jjwxc.net", "ishare.iask.sina.com.cn", "www.cmread.com",
                "www.52ranwen.net", "www.dingdianzw.com", "www.topber.com", "www.391k.com", "www.qqxzb.com",
                "www.zojpw.com", "www.pp8.com", "www.bxwx.org", "www.hrsxb.com", "www.497.com", "www.d8qu.com",
                "www.duwanjuan.com", "www.05935.com", "book.zongheng.com", "www.55x.cn", "www.freexs.cn",
                "xiaoshuo.360.cn", "www.3kw.cc", "www.gzbpi.com", "book.sina.com.cn", "www.vodtw.com", "wenda.so.com",
                "product.dangdang.com", "www.chuiyao.com", "novel.slieny.com", "www.bilibili.com", "donghua.dmzj.com",
                "www.yaojingweiba.com", "www.qb5200.com", "www.520tingshu.com", "www.567zw.com", "www.zjrxz.com",
                "v.qq.com", "www.hackhome.com", "news.fznews.com.cn", "www.le.com"]

# 针对某些网站检索出来的地址和真正的目录地址不一样从而进行替换
REPLACE_RULES = {
    "www.miaobige.com": {
        'old': 'miaobige.com/book/',
        'new': 'miaobige.com/read/'
    },
    "www.5ccc.net": {
        'old': '5ccc.net/wksz_info/',
        'new': '5ccc.net/xiaoshuo/'
    },
    "www.7kankan.com": {
        'old': '7kankan.com/files/article/info/',
        'new': '7kankan.com/files/article/html/'
    },
    "www.xqingdou.net": {
        'old': 'xqingdou.net/book_',
        'new': 'xqingdou.net/chapter_'
    },
    "www.wuyanxia.net": {
        'old': 'wuyanxia.net/book/',
        'new': 'wuyanxia.net/read/'
    },
    "www.263zw.com": {
        'old': '263zw.com/402770/',
        'new': '263zw.com/402770/list/'
    },
}

# 搜索引擎检索优先级
ENGINE_PRIORITY = ['360', 'baidu']

# Rules
Rules = namedtuple('Rules', 'content_url chapter_selector content_selector')
LatestRules = namedtuple('LatestRules', 'plan meta_value selector')

# 获取小说最新章节
PLAN_01 = LatestRules(
    True,
    {'latest_chapter_name': 'og:novel:latest_chapter_name', 'latest_chapter_url': 'og:novel:latest_chapter_url'},
    None,
)

LATEST_RULES = {
    "www.biqugex.com": PLAN_01,
    "www.biquge.tw": PLAN_01,
    "www.qu.la": PLAN_01,
    "www.ybdu.com": PLAN_01,
    "www.wenxuemi.com": PLAN_01,
    "www.biquge.com": PLAN_01,
    "www.23us.cc": PLAN_01,
    "www.xs222.com": PLAN_01,
    "www.lewen8.com": PLAN_01,
    "www.bqg5200.com": PLAN_01,
    "www.vodtw.com": PLAN_01,
    "www.6mao.com": PLAN_01,
    "www.touxiang.la": PLAN_01,
    "www.bxquge.com": PLAN_01,
    "www.beidouxin.com": PLAN_01,
    "www.263zw.com": PLAN_01,
    "www.3qzone.com": PLAN_01,
    "wwww.yooread.com": PLAN_01,
    "www.suimeng.la": PLAN_01,
    "www.bequge.com": PLAN_01,
    "www.biquku.co": PLAN_01,
    "www.xbqge.com": PLAN_01,
    "www.aiquxs.com": PLAN_01,
    "www.23us.com": PLAN_01,
    "www.ddbiquge.com": PLAN_01,
    "www.abocms.cn": PLAN_01,
    "www.liewen.cc": PLAN_01,
    "www.8535.org": PLAN_01,
    "www.dingdianzw.com": PLAN_01,
    "www.biquge.cc": PLAN_01,
    "www.111bz.org": PLAN_01,
    "www.biqugebook.com": PLAN_01,
    "www.e8zw.com": PLAN_01,
    "www.xqqxs.com": PLAN_01,
    "tianyibook.la": PLAN_01,
    "www.lingdianksw.com": PLAN_01,
    "www.qb5.tw": PLAN_01,
    "www.quanben.com": PLAN_01,
    "www.58xs.com": PLAN_01,
    "www.biqukan.com": PLAN_01,
    "www.yssm.org": PLAN_01,
    "www.81zw.com": PLAN_01,
    "www.ymoxuan.com": PLAN_01,
    "www.mytxt.cc": PLAN_01,
    "www.woquge.com": PLAN_01,
    "www.biquguo.com": PLAN_01,
    "www.8jzw.cc": PLAN_01,
    "www.8jzw.com": PLAN_01,

    # 其他规则
    "www.50331.net": LatestRules(
        False,
        None,
        {'content_url': "http://www.50331.net/", 'tag': 'span.zzjie a'}
    )
}

RULES = {
    # demo  'name': Rules('content_url', {chapter_selector}, {content_selector})
    # content_url=1表示章节链接使用本身自带的链接，不用拼接
    # content_url=0表示章节网页需要当前页面url拼接
    # 'www.biqule.com': Rules('www.biqule.com', {'class': 'box_con'},{}),
    # 'www.lingdiankanshu.com': Rules('www.lingdiankanshu.com', {'class': 'box_con'}, {}),
    # 'www.hhlwx.com': Rules('www.hhlwx.co', {'class': 'chapterlist'},{}),
    # 已解析
    'www.biqugex.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.8jzw.com': Rules('http://www.8jzw.com/', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.biquguo.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.woquge.com': Rules('1', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.zhonghuawuxia.com': Rules('1', {'class': 'list'}, {'id': 'content'}),
    # 已解析
    'www.mytxt.cc': Rules('http://www.mytxt.cc/', {'class': 'story_list_m62topxs'}, {'class': 'detail_con_m62topxs'}),
    # 已解析
    'www.136txt.com': Rules('1', {'class': 'directory_con'}, {'id': 'chapterContent'}),
    # 已解析
    'www.xs74.com': Rules('1', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.yssm.org': Rules('0', {'class': 'chapterlist'}, {'id': 'content'}),
    # 已解析
    'www.luoxia.com': Rules('1', {'class': 'book-list'}, {'tag': 'p'}),
    # 已解析
    'www.sbkk88.com': Rules('http://www.sbkk88.com/', {'class': 'leftList'}, {'id': 'f_article'}),
    # 已解析
    'www.dxsxs.com': Rules('http://www.dxsxs.com/', {'id': 'yuedu'}, {'class': 'zw'}),
    # 已解析
    'www.wenku8.com': Rules('0', {'class': 'css'}, {'id': 'content'}),
    # 已解析
    'www.xqingdou.net': Rules('http://www.xqingdou.net/', {'class': 'dirconone'}, {'id': 'chapter_content'}),
    # 已解析
    'www.zuowe.com': Rules('http://www.zuowe.com/', {'class': 'book_list'}, {'id': 'htmlContent'}),
    # 已解析
    'www.wuyanxia.net': Rules('http://www.wuyanxia.net/', {'class': 'zjlist4'}, {'id': 'htmlContent'}),
    # 已解析
    'www.50331.net': Rules('http://www.50331.net/', {'id': 'main'}, {'class': 'zhang-txt-nei-rong'}),
    # 已解析
    'www.wenxuemi.com': Rules('http://www.wenxuemi.com/', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.xs222.com': Rules('http://www.xs222.com/', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.lewen8.com': Rules('http://www.lewen8.com/', {'id': 'chapterlist'}, {'id': 'content'}),
    # 已解析
    'www.5ccc.net': Rules('0', {'class': 'acss'}, {'id': 'content'}),
    # 已解析
    'www.suimeng.la': Rules('0', {'class': 'acss'}, {'id': 'ccontent'}),
    # 已解析
    'www.bqg5200.com': Rules('http://www.bqg5200.com/', {'id': 'readerlist'}, {'id': 'content'}),
    # 已解析
    'www.vodtw.com': Rules('0', {'class': 'insert_list'}, {'class': 'contentbox'}),
    # 已解析
    'www.6mao.com': Rules('http://www.6mao.com/', {'class': 'liebiao_bottom'}, {'id': 'neirong'}),
    # 已解析
    'www.touxiang.la': Rules('http://www.touxiang.la/', {'class': 'listmain'}, {'id': 'content'}),
    # 已解析
    'www.7kankan.com': Rules('0', {'class': 'uclist'}, {'id': 'content'}),
    # 已解析
    'www.biqugetw.com': Rules('http://www.biqugetw.com/', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'gdbzkz.com': Rules('1', {'class': 'mulu'}, {'class': 'content-body'}),
    # 已解析
    'www.gdbzkz.com': Rules('1', {'class': 'mulu'}, {'class': 'content-body'}),
    # 已解析
    'www.freexs.cn': Rules('0', {'class': 'readout'}, {'class': 'shuneirong'}),
    # 已解析
    'www.bxquge.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.beidouxin.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.3qzone.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.97xs.net': Rules('1', {'class': 'box'}, {'id': 'htmlContent'}),
    # 已解析
    'www.7dsw.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.263zw.com': Rules('1', {'class': 'chapter'}, {'id': 'chapterContent'}),
    # 已解析
    'www.biquge5.com': Rules('1', {'id': 'chapterslist'}, {'id': 'content'}),
    # 已解析
    'www.yooread.com': Rules('http://www.yooread.com', {'id': 'chapterList'}, {'tag': 'p'}),
    # 已解析
    'www.xs82.com': Rules('0', {'class': 'chapterlist'}, {'id': 'content'}),
    # 已解析
    'www.kanshuhai.com': Rules('0', {'id': 'book'}, {'id': 'content'}),
    # 已解析
    'www.bequge.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析  请求失败
    # 'www.biquge5200.com': Rules('1', {'id': 'list'}, {'id': 'content'}),
    # 已解析
    'www.biquku.co': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.xbqge.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.aiquxs.com': Rules('0', {'id': 'list'}, {'id': 'booktext'}),
    # 已解析
    # 'www.piaotian.com': Rules('0', {'class': 'centent'}, {'class': 'fonts_mesne'}),
    # 已解析
    'www.ttshu.com': Rules('http://www.ttshu.com', {'class': 'border'}, {'id': 'content'}),
    # 已解析
    'www.23us.com': Rules('0', {'id': 'at'}, {'id': 'contents'}),
    # 已解析
    'www.23wx.cc': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.ddbiquge.com': Rules('http://www.ddbiquge.com', {'class': 'listmain'}, {'id': 'content'}),
    # 已解析
    'www.abocms.cn': Rules('http://www.abocms.cn', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.liewen.cc': Rules('http://www.liewen.cc', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.heiyange.com': Rules('http://www.heiyange.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.8535.org': Rules('0', {'class': 'booklist'}, {'class': 'txtc'}),
    # 已解析
    'www.dingdianzw.com': Rules('http://www.dingdianzw.com', {'id': 'bgdiv'}, {'id': 'content'}),
    # 已解析
    'www.biquge.cc': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.lewenxiaoshuo.com': Rules('1', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.111bz.org': Rules('http://www.111bz.org', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.biqugebook.com': Rules('http://www.biqugebook.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.e8zw.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.xqqxs.com': Rules('0', {'class': 'box_con'}, {'class': 'content'}),
    # 已解析
    'www.139book.com': Rules('http://www.139book.com', {'class': 'list_box'}, {'class': 'box_box'}),
    # 已解析
    'www.jcdf99.com': Rules('0', {'class': 'list_box'}, {'id': 'content'}),
    # 已解析
    'www.tianzeba.com': Rules('http://www.tianzeba.com', {'class': 'chapterlist'}, {'id': 'BookText'}),
    # 已解析
    'www.kanshuwangzhan.com': Rules('0', {'id': 'chapterlist'}, {'id': 'booktext'}),
    # 已解析
    'tianyibook.la': Rules('http://tianyibook.la', {'class': 'chapterlist'}, {'id': 'BookText'}),
    # 已解析
    'www.quanben.net': Rules('http://www.quanben.net', {'class': 'chapterlist'}, {'id': 'BookText'}),
    # 已解析
    # 'www.zhetian.org': Rules('http://www.zhetian.org', {'class': 'body '}, {'class': 'content'}),
    # 已解析
    'www.lingdianksw.com': Rules('0', {'class': 'acss'}, {'id': 'ccontent'}),
    # 已解析
    'www.qb5.tw': Rules('http://www.qb5.tw', {'class': 'zjbox'}, {'id': 'content'}),
    # 已解析
    'www.ybdu.com': Rules('0', {'class': 'mulu_list'}, {'id': 'htmlContent'}),
    # 已解析
    'www.quanben.com': Rules('0', {'class': 'mulu_list'}, {'id': 'htmlContent'}),
    # 已解析
    'www.fhxs.com': Rules('1', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.biquge.biz': Rules('http://www.biquge.biz', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.58xs.com': Rules('http://www.58xs.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.biqukan.com': Rules('http://www.biqukan.com', {'class': 'listmain'}, {'id': 'content'}),
    # 已解析
    'www.shuyuelou.com': Rules('http://www.shuyuelou.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.mangg.com': Rules('http://www.mangg.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.50zw.com': Rules('0', {'class': 'chapterlist'}, {'id': 'htmlContent'}),
    # 已解析
    'www.lingdiankanshu.co': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.biqiku.com': Rules('http://www.biqiku.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.duilianku.com': Rules('http://www.duilianku.com', {'id': 'list'}, {'class': 'chapter'}),
    # 已解析
    'www.5xiaxiaoshuo.com': Rules('http://www.5xiaxiaoshuo.com', {'class': 'art_listmain_main'}, {'id': 'content'}),
    # 已解析
    'www.81xsw.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.wxguan.com': Rules('http://www.wxguan.com', {'class': 'listmain'}, {'id': 'content'}),
    # 已解析
    'www.qb5200.tw': Rules('http://www.qb5200.tw', {'class': 'listmain'}, {'id': 'content'}),
    # 已解析
    'www.fox2008.cn': Rules('http://www.fox2008.cn', {'class': 'book'}, {'id': 'chapterContent'}),
    # 已解析
    'www.22zw.com': Rules('0', {'class': 'acss'}, {'id': 'content'}),
    # 已解析
    'www.k6uk.com': Rules('0', {'class': 'acss'}, {'id': 'content'}),
    # 已解析
    'www.126shu.com': Rules('http://www.126shu.com', {'id': 'list'}, {'id': 'content'}),
    # 已解析
    'www.kooxs.com': Rules('0', {'class': 'list'}, {'id': 'content'}),
    # 已解析
    'www.shubaotxt.com': Rules('0', {'class': 'list'}, {'id': 'content'}),
    # 已解析
    'www.muyuge.com': Rules('1', {'id': 'xslist'}, {'id': 'content'}),
    # 已解析
    # 'www.daizhuzai.com': Rules('http://www.daizhuzai.com', {'class': 'dirlist'}, {'class': 'content'}),
    # 已解析
    'www.biqu.la': Rules('0', {'class': 'book_list'}, {'id': 'htmlContent'}),
    # 已解析
    'shushu.com.cn': Rules('http://shushu.com.cn', {'id': 'dirsort01'}, {'id': 'content'}),
    # 已解析
    'www.shuhai.com': Rules('0', {'class': 'box_chap'}, {'id': 'readcon'}),
    # 已解析
    'www.37yue.com': Rules('0', {'class': 'list-chapter'}, {'class': 'chapter'}),
    # 已解析
    'www.35zw.com': Rules('0', {'class': 'book_list'}, {'id': 'htmlContent'}),
    # 已解析
    'www.xinshu.in': Rules('http://www.xinshu.in', {'class': 'list_box'}, {'class': 'box_box'}),
    # 已解析
    'www.lwxs520.com': Rules('0', {'class': 'dccss'}, {'id': 'content'}),
    # 已解析
    'www.lwxs.la': Rules('http://www.lwxs.la', {'id': 'defaulthtml4'}, {'id': 'content'}),
    # 已解析
    'www.biqule.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.33yq.com': Rules('1', {'class': 'box_con'}, {'class': 'zhangjieTXT'}),
    # 已解析
    'www.dishuge.com': Rules('1', {'class': 'update'}, {'tag': 'p'}),
    # 已解析
    'www.qu.la': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.shuge.net': Rules('http://www.shuge.net', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.daomengren.com': Rules('http://www.daomengren.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.81zw.net': Rules('http://www.81zw.net', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.09xs.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.fhxiaoshuo.com': Rules('1', {'class': 'box_con'}, {'class': 'zhangjieTXT'}),
    # 已解析
    'www.yikanxiaoshuo.com': Rules('http://www.yikanxiaoshuo.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.1xiaoshuo.com': Rules('http://www.1xiaoshuo.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.kanshu.la': Rules('http://www.kanshu.la', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.kbiquge.com': Rules('http://www.kbiquge.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.00ksw.net': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.booktxt.net': Rules('http://www.booktxt.net', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'wanmeishijiexiaoshuo.org': Rules('1', {'class': 'bg'}, {'class': 'content'}),
    # 已解析
    'www.sosoxiaoshuo.cc': Rules('http://www.sosoxiaoshuo.cc', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.ciluke.com': Rules('0', {'id': 'list'}, {'id': 'content'}),
    # 已解析
    'www.81zw.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.cilook.net': Rules('0', {'id': 'cl_content'}, {'id': 'content'}),
    # 已解析
    'www.baoliny.com': Rules('1', {'class': 'readerListShow'}, {'id': 'content'}),
    # 已解析
    'www.biquge.tw': Rules('http://www.biquge.tw', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.7788xs.net': Rules('http://www.7788xs.net', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.06sy.com': Rules('http://www.06sy.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.biqumo.com': Rules('http://www.biqumo.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.kanshuzhe.com': Rules('http://www.kanshuzhe.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.biqiuge.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.lwxs.com': Rules('0', {'class': 'box_con'}, {'id': 'TXT'}),
    # 已解析
    'www.biqugezw.com': Rules('http://www.biqugezw.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析 经常跳到无法预料的网站  故禁止
    # 'www.is028.cn': Rules('http://www.biquge.com.tw', {'class': 'box_con'}, {'id': 'content'}),
    # www.is028.cn会跳转到http://www.biquge.com.tw
    'www.biquge.com.tw': Rules('http://www.biquge.com.tw', {'class': 'box_con'}, {'id': 'content'}),
    # 'www.xs82.com': Rules('-1', {'class': 'chapterlist'}, {'id': 'content'}),
    # 已解析
    'www.shuqizw.com': Rules('http://www.shuqizw.com', {'class': 'article_texttitleb'}, {'id': 'book_text'}),
    # 已解析
    'read.ixdzs.com': Rules('0', {'class': 'catalog'}, {'class': 'content'}),
    # 已解析
    'www.shumilou.net': Rules('0', {'class': 'chapterlist'}, {'id': 'BookText'}),
    # 已解析
    'www.8shuw.com': Rules('1', {'class': 'chapterlist'}, {'id': 'readtext'}),
    # 已解析
    # 'www.ttshu.com': Rules('http://www.ttshu.com', {'class': 'border'}, {'id': 'content'}),
    # 已解析
    'www.heiyan.la': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.bbsa5.com': Rules('1', {'class': 'panel'}, {'class': 'content-body'}),
    # 已解析
    'www.tycqxs.com': Rules('http://www.tycqxs.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.miaobige.com': Rules('0', {'id': 'readerlists'}, {'id': 'content'}),
    # 已解析
    'www.dashubao.net': Rules('0', {'class': 'ml_main'}, {'class': 'yd_text2'}),
    # 已解析
    'www.23zw.com': Rules('0', {'id': 'chapter_list'}, {'id': 'text_area'}),
    # 已解析
    'www.23us.la': Rules('http://www.23us.la', {'class': 'inner'}, {'id': 'content'}),
    # 已解析
    'www.2952.cc': Rules('0', {'class': 'inner'}, {'id': 'content'}),
    # 已解析
    'www.23us.cc': Rules('0', {'class': 'inner'}, {'id': 'content'}),
    # 已解析
    'www.13xs.com': Rules('0', {'class': 'box_con'}, {'id': 'booktext'}),
    # 已解析
    'www.tsxsw.com': Rules('0', {'class': 'bdsub'}, {'id': 'contents'}),
    # 已解析
    'www.ymoxuan.com': Rules('1', {'class': 'mulu'}, {'id': 'content'}),
    # 已解析
    'zetianjiba.net': Rules('1', {'class': 'bg'}, {'class': 'content'}),
    # 已解析
    'www.37zw.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.555zw.com': Rules('0', {'class': 'dir'}, {'id': 'content'}),
    # 已解析
    'www.jueshitangmen.info': Rules('1', {'class': 'bg'}, {'class': 'content'}),
    # 已解析
    'www.bxwx9.org': Rules('0', {'class': 'TabCss'}, {'id': 'content'}),
    # 已解析
    'www.xxbiquge.com': Rules('http://www.xxbiquge.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.fs23.com': Rules('http://www.fs23.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.longtengx.com': Rules('http://www.longtengx.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.lingyu.org': Rules('http://www.lingyu.org', {'class': 'mt10'}, {'id': 'htmlContent'}),
    # 已解析
    'www.aszw8.com': Rules('0', {'id': 'at'}, {'id': 'contents'}),
    # 已解析
    'www.23us.so': Rules('1', {'id': 'at'}, {'id': 'contents'}),
    # 已解析
    'www.biquge.lu': Rules('http://www.biquge.lu', {'class': 'listmain'}, {'id': 'content'}),
    # 已解析
    'www.3zm.net': Rules('http://www.3zm.net', {'class': 'listmain'}, {'id': 'content'}),
    # 已解析
    'www.biquge.com': Rules('http://www.biquge.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.kanshuzhong.com': Rules('0', {'class': 'bookcontent'}, {'class': 'textcontent'}),
    # 已解析
    'www.siluke.tw': Rules('http://www.siluke.tw', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    # 'www.ttshu.com': Rules('http://www.ttshu.com', {'class': 'border'}, {'id': 'content'}),

}
