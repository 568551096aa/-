# -
类似按键精灵的屏幕找图，但是按键精灵的屏幕找图不好用，就用python的cv做了一个 主要是自己用
简单做了一个界面，点击开始或者小键盘1开始，点击结束或者小键盘2结束

代码也都做了注释，主要几个部分 1、通过标题找到窗口坐标和大小
2、cv写的模版匹配，加上了把图片周围四个点作为背景色的代码，这样可以手动处理图片提高识别成功率(手动就是把你认为是背景的都手动涂改为同一个颜色)；
本来想做成神经网络的但是需要训练的图片目前我不知道又通过一两张图片可以识别的好的办法了
3、写了一个界面，开始和结束按钮，有快捷键绑定，可以加音效但是要音效文件（我还没试）

注：有了gpt以后像这种简易的代码都可以快速搞定，这让我深深为程序员同行们感到担忧呀
