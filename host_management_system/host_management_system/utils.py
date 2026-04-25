from typing import Dict, List, Any
import secrets
import string

from django.core.signing import dumps, loads


def check_need_params(body: Dict[str, Any], need_params: List[str]) -> List[str]:
    """验证参数合法性"""
    exist_params = []
    for k, v in body.items():
        if k in need_params and v:
            exist_params.append(k)
    miss_params = list(set(need_params) - set(exist_params))
    return miss_params


def generate_password(length: int = 10):
    """密码生成（默认长度为 10）"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def encrypt_password(password: str) -> str:
    """加密密码"""
    return dumps(password, salt='host-password')


def decrypt_password(encrypted_password: str) -> str:
    """解密密码"""
    return loads(encrypted_password, salt='host-password')
