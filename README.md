# pixivindex 本地图片管理
<h2>搜图api需要改进</h2>
<h2>浏览器对大量图片渲染速度较慢，需要另外开发前端</h2>
<div class="divider"></div>
<p>本项目的大致目标：</p>
<p>使用python脚本搜索图片，构建本地图片数据库，方便对图片进行分类、搜索。</p>
<p>使用效果:</p>
<img src="http://azusebox.moe/wp-content/uploads/2018/09/2018-09-12-5.png" alt="">
<img src="http://azusebox.moe/wp-content/uploads/2018/09/2018-09-12-6.png" alt="">

<p>目前使用的图片搜索服务：http://www.iqdb.org</p>
<p>***识别率并不高，求推荐更好的搜图api***</p>

<div class="divider"></div>
<p>搭建流程：</p>
<p>（1）修改python脚本picindex.py中的目录为您的图片库目录</p>
<p>（2）建立数据库，并设置python脚本中数据库名和表名，表结构如图</p>
<img src="http://azusebox.moe/wp-content/uploads/2018/09/2018-09-12-7.png" alt="">
<p>（3）运行python脚本，等待图片搜索完成建立数据库</p>
<p>     数据库内容例：</p>
<img src="http://azusebox.moe/wp-content/uploads/2018/09/2018-09-12-8.png" alt="">
<p>     所有进行过搜索尝试的图片就会被记录，下次再运行脚本时自动跳过</p>
<p>     state分为tagged(搜索完成 有记录) notfound(未找到) error(搜索时脚本出错)</p>
<p>（4）建立数据库后将两个php文件放到localhost的根目录下，打开index.html（直接在文件浏览器中打开，在localhost中打开会无法访问本地图片文件）</p>
<p>enjoy(x</p>

