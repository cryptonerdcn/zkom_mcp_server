# ZKOM MCP服务器安装指南

本指南将帮助您安装和配置ZKOM MCP服务器，以便在Claude或其他支持MCP的AI助手中使用。

## 前提条件

- Python 3.8+
- pip
- Git

## 安装步骤

### 1. 获取代码

克隆GitHub仓库：

```bash
git clone https://github.com/your-username/zkom_mcp_server.git
cd zkom_mcp_server
```

### 2. 安装服务器

使用pip安装：

```bash
pip install -e .
```

这会将`zkom-mcp-server`命令安装到您的系统。

### 3. 使用服务器

您可以通过以下方式启动服务器：

```bash
# 作为命令行工具
zkom-mcp-server

# 或作为Python模块
python -m app.main
```

## 在Claude中配置MCP服务器

要在Claude中使用ZKOM MCP服务器，请将以下配置添加到Claude的配置文件中：

```json
{
  "mcpServers": {
    "crypto-price": {
      "command": "zkom-mcp-server",
      "env": {
        "PORT": "8000",
        "HOST": "0.0.0.0",
        "COINBASE_API_URL": "https://api.coinbase.com/v2/exchange-rates"
      }
    }
  }
}
```

## 配置选项

ZKOM MCP服务器支持以下环境变量：

- `PORT`: 服务器端口（默认：8000）
- `HOST`: 服务器主机地址（默认：0.0.0.0）
- `COINBASE_API_URL`: Coinbase API URL（默认：https://api.coinbase.com/v2/exchange-rates）
- `CACHE_TTL`: 缓存过期时间（秒）（默认：60）

## 验证安装

安装后，您可以通过访问以下URL验证服务器是否正常运行：

```
http://localhost:8000/health
```

如果看到包含`"status": "ok"`的JSON响应，说明服务器已成功安装并运行。

## 故障排除

如果遇到问题，请检查：

1. Python版本是否满足要求（3.8+）
2. 所有依赖包是否正确安装
3. 端口8000是否已被其他应用占用
4. 日志中是否有错误信息

## 了解更多

有关ZKOM MCP服务器的更多信息，请查看文档或访问我们的GitHub仓库。

## Model Context Protocol (MCP)介绍

MCP是一个允许AI模型与外部服务进行交互的协议，使模型能够访问实时数据、执行计算或与各种API交互。Claude和其他现代AI助手使用MCP协议连接到外部工具和服务。

您可以在以下地址了解更多关于MCP的信息：
https://github.com/anthropics/anthropic-cookbook/tree/main/mcp 