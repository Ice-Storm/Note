Blog 维护日记
============

#2015-2-22
修复了一直以来代码块背景色无法设置的问题，在pygments.css头部添加了两行：
```css
.highlight pre { background-color: #49483e}
.highlight pre .language-text { color: white}
```
造成这个问题似乎说是float div引起的，但是本人不是前端开发的，所以暂时无法深究。

#2015-3-23
修改了css中h1,h2,h3的大小。