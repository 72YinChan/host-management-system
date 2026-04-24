from typing import Dict, List, Any


def check_need_params(body: Dict[str, Any], need_params: List[str]) -> List[str]:
    """验证参数合法性"""
    exist_params = []
    for k, v in body.items():
        if k in need_params and v:
            exist_params.append(k)
    miss_params = list(set(need_params) - set(exist_params))
    return miss_params
