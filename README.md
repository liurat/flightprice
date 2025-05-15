# 机票价格监控工具

这是一个自动监控机票价格的工具，可以定期抓取指定航线的机票价格信息。

## 功能特点

- 自动监控指定航线的机票价格
- 支持定时执行（默认每6小时执行一次）
- 自动保存数据到Excel文件
- 支持Windows系统运行
- 无需Python环境即可运行

## 使用方法

1. 下载最新版本的发布包（在GitHub Actions的Artifacts中）
2. 解压下载的文件
3. 双击`start_monitor.bat`启动程序
4. 程序会在后台运行，自动执行爬虫任务
5. 数据将保存在Excel文件中

## 配置说明

可以通过修改`scheduler_config.py`文件来调整以下设置：

- `SCHEDULER_INTERVAL`：执行间隔（小时）
- `RUN_IMMEDIATELY`：是否在启动时立即执行一次
- `LOG_FILE`：日志文件路径
- `LOG_FORMAT`：日志格式

## 注意事项

1. 程序运行时会在控制台显示运行状态
2. 如果要停止程序，可以按Ctrl+C或直接关闭控制台窗口
3. 程序会自动处理错误并继续运行
4. 所有的日志都会保存在`scheduler.log`文件中

## 开发说明

如果需要修改代码，请确保安装了所有依赖：

```bash
pip install -r requirements.txt
```

## 许可证

MIT License 