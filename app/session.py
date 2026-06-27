"""
会话管理 — JSON 持久化

支持：
- 创建/读取/保存/删除会话
- 过期清理
- 断点续跑
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

from .models import AnalyzeContext

SESSION_DIR = os.path.join(os.path.dirname(__file__), "instance", "sessions")
SESSION_TTL_HOURS = 168  # 7 天过期


def _ensure_session_dir() -> None:
    """确保会话目录存在。"""
    os.makedirs(SESSION_DIR, exist_ok=True)


def _session_path(session_id: str) -> str:
    """会话文件路径。"""
    return os.path.join(SESSION_DIR, f"{session_id}.json")


def create_session(project_name: str, config_snapshot: dict = None) -> AnalyzeContext:
    """创建新会话。"""
    _ensure_session_dir()
    session_id = str(uuid.uuid4())
    ctx = AnalyzeContext(
        session_id=session_id,
        project_name=project_name,
        config_snapshot=config_snapshot or {},
    )
    save_session(ctx)
    return ctx


def get_session(session_id: str) -> Optional[AnalyzeContext]:
    """读取会话。"""
    path = _session_path(session_id)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return AnalyzeContext.from_dict(data)


def save_session(ctx: AnalyzeContext) -> None:
    """保存会话。"""
    _ensure_session_dir()
    path = _session_path(ctx.session_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(ctx.to_dict(), f, ensure_ascii=False, indent=2)


def delete_session(session_id: str) -> bool:
    """删除会话。"""
    path = _session_path(session_id)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def list_sessions(limit: int = 20) -> list:
    """列出最近会话。"""
    _ensure_session_dir()
    sessions = []
    for fname in os.listdir(SESSION_DIR):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(SESSION_DIR, fname)
        try:
            with open(fpath, encoding="utf-8") as f:
                data = json.load(f)
            sessions.append({
                "session_id": data.get("session_id", fname.replace(".json", "")),
                "project_name": data.get("project_name", "未知项目"),
                "created_at": data.get("created_at", ""),
                "current_tier": data.get("current_tier", ""),
                "current_step": data.get("current_step", ""),
                "step_count": len(data.get("steps", {})),
            })
        except Exception:
            continue
    sessions.sort(key=lambda x: x["created_at"], reverse=True)
    return sessions[:limit]


def cleanup_expired_sessions() -> int:
    """清理过期会话。"""
    _ensure_session_dir()
    cutoff = datetime.now() - timedelta(hours=SESSION_TTL_HOURS)
    cleaned = 0
    for fname in os.listdir(SESSION_DIR):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(SESSION_DIR, fname)
        try:
            with open(fpath, encoding="utf-8") as f:
                data = json.load(f)
            created = datetime.fromisoformat(data.get("created_at", ""))
            if created < cutoff:
                os.remove(fpath)
                cleaned += 1
        except Exception:
            continue
    return cleaned