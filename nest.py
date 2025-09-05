def convert_to_nested_dict(assignments):
    """
    将点分格式的赋值转换为嵌套字典（支持多种输入格式）
    
    Args:
        assignments: 可以是以下格式之一：
                    1. 列表: [("a.b.c", "1Gi"), ("a.b.d", "2Gi")]
                    2. 字典: {"a.b.c": "1Gi", "a.b.d": "2Gi"}
                    3. 字符串: "a.b.c=1Gi,a.b.d=2Gi"
    
    Returns:
        dict: 转换后的嵌套字典
    """
    def set_nested_value(d, keys, value):
        if len(keys) == 1:
            d[keys[0]] = value
        else:
            if keys[0] not in d:
                d[keys[0]] = {}
            set_nested_value(d[keys[0]], keys[1:], value)
    
    result = {}
    
    # 处理不同类型的输入
    # if isinstance(assignments, str):
    #     # 字符串格式: "a.b.c=1Gi,a.b.d=2Gi"
    #     for assignment in assignments.split(','):
    #         if '=' in assignment:
    #             key_path, value = assignment.split('=', 1)
    #             keys = key_path.strip().split('.')
    #             clean_value = value.strip().strip('"\'')
    #             set_nested_value(result, keys, clean_value)
    
    if isinstance(assignments, dict):
        # 字典格式: {"a.b.c": "1Gi"}
        for key_path, value in assignments.items():
            keys = key_path.split('.')
            set_nested_value(result, keys, value)
    
    # elif isinstance(assignments, list):
    #     # 列表格式: [("a.b.c", "1Gi")]
    #     for key_path, value in assignments:
    #         keys = key_path.split('.')
    #         set_nested_value(result, keys, value)
    
    return result
# 使用示例
if __name__ == "__main__":
    # 测试不同输入格式
    test_cases = [
        {"a.b.c": "1Gi", "a.b.d": "2Gi"},
        {"sentinel.service.type": "LoadBalancer", "sentinel.service.ip": "1.1.1.1"}
    ]
    
    for i, test_case in enumerate(test_cases):
        result = convert_to_nested_dict(test_case)
        print(f"测试 {i+1}: {result}")