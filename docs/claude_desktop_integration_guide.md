# Claude Desktop集成指南：连接到ZKOM MCP服务器

本指南将帮助您将Claude Desktop与ZKOM MCP服务器集成，以便在Claude中获取加密货币的价格信息。

## 前提条件

- ZKOM MCP服务器已部署并运行（默认地址: http://localhost:8000）
- Claude Desktop已安装
- Python 3.9+

## 安装步骤

### 1. 安装必要的Python包

```bash
pip install httpx asyncio
```

### 2. 复制集成文件

将以下文件复制到Claude Desktop的插件目录中：

- `adapters/claude_desktop_adapter.py`
- `adapters/claude_desktop_plugin.py`
- `adapters/claude_desktop_config.json`

Claude Desktop的插件目录通常位于：
- Windows: `%APPDATA%\Claude\plugins`
- macOS: `~/Library/Application Support/Claude/plugins`
- Linux: `~/.config/Claude/plugins`

### 3. 配置MCP服务器连接

编辑`claude_desktop_config.json`文件，设置MCP服务器的URL：

```json
{
  "mcp_server": {
    "url": "http://your-mcp-server-address:8000/api/v1/mcp",
    "service_name": "claude.desktop.client",
    "version": "1.0",
    "timeout": 30.0
  },
  ...
}
```

### 4. 启用插件

1. 打开Claude Desktop
2. 进入设置 > 插件
3. 启用"加密货币价格"插件
4. 重启Claude Desktop

## 使用方法

### 基本使用

在Claude Desktop中，您可以使用以下命令获取加密货币价格：

```
/crypto-price BTC
```

或者获取多个加密货币的价格：

```
/crypto-price BTC ETH SOL
```

指定基础货币：

```
/crypto-price BTC --currency EUR
```

### 高级设置

您可以通过编辑`claude_desktop_config.json`配置以下选项：

- `watch_list`：默认关注的加密货币列表
- `default_currency`：默认基础货币
- `refresh_interval`：价格刷新间隔（秒）
- `ui`：界面设置
- `logging`：日志设置

## 创建快捷方式

您可以在Claude Desktop中创建快捷方式，方便快速访问加密货币价格：

1. 进入设置 > 快捷方式
2. 点击"添加快捷方式"
3. 设置快捷方式：
   - 名称：加密货币价格
   - 命令：/crypto-price BTC ETH
   - 快捷键：Ctrl+Alt+C（可选）

## 故障排除

如果遇到连接问题，请检查：

1. MCP服务器是否正在运行
2. 配置文件中的URL是否正确
3. 网络连接是否正常
4. 检查Claude Desktop的日志文件（位于插件目录中的`claude_mcp_client.log`）

## API参考

插件提供了以下功能：

- 获取单个加密货币价格
- 获取多个加密货币价格
- 支持不同的基础货币
- 自动刷新价格数据

有关MCP协议的更多信息，请参阅ZKOM MCP服务器文档。

## 开发者资源

如果您想扩展插件功能，可以参考：

- `claude_desktop_adapter.py`：MCP客户端适配器
- `claude_desktop_plugin.py`：Claude Desktop插件实现

您可以通过修改这些文件来添加新功能或修改现有功能。

## 支持

如有问题，请访问我们的GitHub项目页面：
https://github.com/your-username/zkom_mcp_server 