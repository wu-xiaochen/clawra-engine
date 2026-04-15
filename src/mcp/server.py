"""
Clawra MCP Server

为 Claude Code 提供 Clawra 的记忆和推理能力。
通过 Model Context Protocol (MCP) 暴露 Clawra 的核心功能。

启动方式:
    python -m clawra.mcp.server

Claude Code 配置 (.claude/mcp.json):
    {
        "mcpServers": {
            "clawra": {
                "command": "python",
                "args": ["-m", "clawra.mcp.server"]
            }
        }
    }
"""

import json
import logging
import sys
import os
from typing import Any, Dict, List, Optional
from pathlib import Path

# 将 src 加入 path 以便导入 clawra
SRC_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SRC_ROOT))

from src.clawra import Clawra
from src.core.reasoner import Fact

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# MCP Protocol Versions
MCP_VERSION = "2024-11-05"


class ClawraMCPServer:
    """
    Clawra MCP Server
    
    通过 stdio 暴露以下工具:
    - clawra_learn: 从文本学习知识
    - clawra_reason: 执行神经符号推理
    - clawra_add_fact: 添加事实三元组
    - clawra_query_patterns: 查询学习到的模式
    - clawra_retrieve: GraphRAG 知识检索
    - clawra_evolve: 触发自主进化闭环
    - clawra_stats: 获取系统统计
    """

    def __init__(self):
        self.clawra: Optional[Clawra] = None
        self._initialize_clawra()

    def _initialize_clawra(self):
        """初始化 Clawra 实例"""
        try:
            self.clawra = Clawra()
            logger.info("✅ Clawra MCP Server 初始化成功")
        except Exception as e:
            logger.error(f"❌ Clawra 初始化失败: {e}")
            self.clawra = None

    def _jsonrpc_response(self, id: Any, result: Any) -> Dict:
        """构造 JSON-RPC 响应"""
        return {
            "jsonrpc": "2.0",
            "id": id,
            "result": result
        }

    def _jsonrpc_error(self, id: Any, code: int, message: str) -> Dict:
        """构造 JSON-RPC 错误响应"""
        return {
            "jsonrpc": "2.0",
            "id": id,
            "error": {
                "code": code,
                "message": message
            }
        }

    # ─────────────────────────────────────────────────────────────
    # MCP Handlers
    # ─────────────────────────────────────────────────────────────

    def handle_initialize(self, id: Any, params: Dict) -> Dict:
        """MCP 初始化握手"""
        return self._jsonrpc_response(id, {
            "protocolVersion": MCP_VERSION,
            "capabilities": {
                "tools": {
                    "listChanged": True
                }
            },
            "serverInfo": {
                "name": "clawra",
                "version": "4.2.0"
            }
        })

    def handle_tools_list(self, id: Any, params: Dict) -> Dict:
        """列出所有可用工具"""
        tools = [
            {
                "name": "clawra_learn",
                "description": "从自然语言文本中自动学习知识规则。输入一段文本，Clawra 会自动提取实体、关系和约束，存入知识图谱。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "要学习的自然语言文本"
                        },
                        "domain_hint": {
                            "type": "string",
                            "description": "领域提示（可选），帮助更准确地提取知识"
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "clawra_add_fact",
                "description": "手动添加事实三元组到知识图谱。用于显式地记录实体之间的关系。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string", "description": "主语实体"},
                        "predicate": {"type": "string", "description": "谓词/关系"},
                        "object": {"type": "string", "description": "宾语实体"},
                        "confidence": {
                            "type": "number",
                            "description": "置信度 (0-1)，默认 0.9"
                        }
                    },
                    "required": ["subject", "predicate", "object"]
                }
            },
            {
                "name": "clawra_reason",
                "description": "执行神经符号混合推理。从已有事实出发，通过前向链逻辑推导出新结论。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "查询语句或推理目标"
                        },
                        "max_depth": {
                            "type": "integer",
                            "description": "推理深度，默认 3",
                            "default": 3
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "clawra_query_patterns",
                "description": "查询知识图谱中已学习的模式/规则。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": "按领域过滤（可选）"
                        },
                        "keyword": {
                            "type": "string",
                            "description": "按关键词搜索（可选）"
                        }
                    }
                }
            },
            {
                "name": "clawra_retrieve",
                "description": "使用 GraphRAG 混合检索从知识库中检索相关内容。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "检索查询"
                        },
                        "top_k": {
                            "type": "integer",
                            "description": "返回结果数量，默认 5",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "clawra_evolve",
                "description": "触发 Clawra 的 8 阶段自主进化闭环。让系统自动评估知识质量、检测冲突、蒸馏技能。",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "clawra_stats",
                "description": "获取 Clawra 系统的统计信息，包括事实数量、模式数量、记忆统计等。",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "clawra_orchestrate",
                "description": "完整的认知编排：检索 + 推理 + 思维链路。适合需要完整认知过程的复杂查询。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "用户查询"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
        return self._jsonrpc_response(id, {"tools": tools})

    def handle_tools_call(self, id: Any, params: Dict) -> Dict:
        """处理工具调用"""
        if self.clawra is None:
            return self._jsonrpc_error(id, -32603, "Clawra 未初始化")

        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        try:
            if tool_name == "clawra_learn":
                result = self.clawra.learn(
                    text=arguments["text"],
                    domain_hint=arguments.get("domain_hint")
                )
            elif tool_name == "clawra_add_fact":
                self.clawra.add_fact(
                    subject=arguments["subject"],
                    predicate=arguments["predicate"],
                    obj=arguments["object"],
                    confidence=arguments.get("confidence", 0.9)
                )
                result = {"status": "success", "message": f"已添加: {arguments['subject']} {arguments['predicate']} {arguments['object']}"}
            elif tool_name == "clawra_reason":
                # 先添加查询为事实（如果需要）
                result = self.clawra.orchestrate(arguments["query"])
            elif tool_name == "clawra_query_patterns":
                patterns = self.clawra.query_patterns(
                    domain=arguments.get("domain"),
                    keyword=arguments.get("keyword")
                )
                result = {"patterns": patterns, "count": len(patterns)}
            elif tool_name == "clawra_retrieve":
                context = self.clawra.retrieve_context(
                    query=arguments["query"],
                    top_k=arguments.get("top_k", 5)
                )
                result = {"context": context, "query": arguments["query"]}
            elif tool_name == "clawra_evolve":
                import asyncio
                result = asyncio.run(self.clawra.evolve())
            elif tool_name == "clawra_stats":
                stats = self.clawra.get_statistics()
                result = stats
            elif tool_name == "clawra_orchestrate":
                result = self.clawra.orchestrate(arguments["query"])
            else:
                return self._jsonrpc_error(id, -32601, f"未知工具: {tool_name}")

            return self._jsonrpc_response(id, {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]})
        except Exception as e:
            logger.error(f"工具调用失败: {tool_name} -> {e}")
            return self._jsonrpc_error(id, -32603, str(e))

    def handle_request(self, method: str, id: Any, params: Dict) -> Dict:
        """路由 MCP 请求"""
        if method == "initialize":
            return self.handle_initialize(id, params)
        elif method == "tools/list":
            return self.handle_tools_list(id, params)
        elif method == "tools/call":
            return self.handle_tools_call(id, params)
        else:
            return self._jsonrpc_error(id, -32601, f"未知方法: {method}")

    def run(self):
        """主循环：读取 stdin，处理 JSON-RPC，写入 stdout"""
        logger.info("🚀 Clawra MCP Server 启动，等待请求...")
        
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
                method = request.get("method", "")
                id = request.get("id")
                params = request.get("params", {})
                
                response = self.handle_request(method, id, params)
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError as e:
                error = self._jsonrpc_error(None, -32700, f"JSON 解析错误: {e}")
                print(json.dumps(error), flush=True)
            except Exception as e:
                error = self._jsonrpc_error(None, -32603, f"服务器错误: {e}")
                print(json.dumps(error), flush=True)


def main():
    """入口点"""
    server = ClawraMCPServer()
    server.run()


if __name__ == "__main__":
    main()
