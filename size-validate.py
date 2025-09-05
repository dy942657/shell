import re
import json
from jsonschema import validate, ValidationError
schema = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "taskmanager": {
            "type": "object",
            "properties": {
                "persistence": {
                    "type": "object",
                    "properties": {
                        "size": {
                            "type": "string",
                            "description": "persistence size",
                            "pattern": r'^(?:[1-9]\d?|[1-4]\d{2}|500)Gi$'
                        }
                    }
                }
            }
        }
    }
}
# 将带单位的存储大小转换为字节数
def convert_to_bytes(size_str):
    """Convert size string with unit to bytes"""
    match = re.match(r"^(\d+(?:\.\d+)?)(Mi|Gi|Ti)$", size_str)
    if not match:
        raise ValueError(f"Invalid size format: {size_str}")
    
    size_val = float(match.group(1))
    unit = match.group(2)
    
    unit_factors = {
        "Mi": 1024**2,   # 1 MiB = 2^20 bytes
        "Gi": 1024**3,   # 1 GiB = 2^30 bytes
        "Ti": 1024**4    # 1 TiB = 2^40 bytes
    }
    
    return size_val * unit_factors[unit]
# 主校验函数
def validate_config(config):
    # 第一步：使用 JSON Schema 校验基本格式
    try:
        validate(instance=config, schema=schema)
    except ValidationError as e:
        return False, f"Schema validation failed: {e.message}"
    
    # 第二步：获取 size 值并进行范围校验
    size_str = config["taskmanager"]["persistence"]["size"]
    
    try:
        bytes_val = convert_to_bytes(size_str)
    except ValueError as e:
        return False, str(e)
    
    # 定义允许的范围（单位：字节）
    min_bytes = 1 * 1024**2     # 1 MiB (2^20)
    max_bytes = 500 * 1024**3   # 500 GiB (2^30 * 500)
    
    if bytes_val < min_bytes:
        return False, f"Size too small ({size_str} < 1Mi)"
    if bytes_val > max_bytes:
        return False, f"Size too large ({size_str} > 500Gi)"
    
    return True, "Validation succeeded"
# 测试配置
if __name__ == "__main__":
    # 有效配置示例
    valid_config = {
        "taskmanager": {
            "persistence": {
                "size": "8Gi"
            }
        },
        "jobmanager": {
            "persistence": {
                "size": "8Gi"
            }
        }
    }
    
    # 无效配置示例（超出范围）
    invalid_config = {
        "taskmanager": {
            "persistence": {
                "size": "600Gi"  # 超过500Gi限制
            }
        }
    }
    
    # 格式错误示例
    bad_format_config = {
        "taskmanager": {
            "persistence": {
                "size": "8GB"  # 单位不符合要求
            }
        }
    }
    
    # 执行校验测试
    print("Valid config test:")
    success, message = validate_config(valid_config)
    print(f"Result: {success}, Message: {message}\n")
    
    print("Invalid config test:")
    success, message = validate_config(invalid_config)
    print(f"Result: {success}, Message: {message}\n")
    
    print("Bad format config test:")
    success, message = validate_config(bad_format_config)
    print(f"Result: {success}, Message: {message}")