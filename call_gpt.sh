#!/bin/bash
# 文件名：run_eval.sh
# 新用法示例：bash run_eval.sh --prompt_type abel --model_dir [PATH] --steps [STEPS] --benchmarks [BENCHMARKS]

# 初始化默认值
PROMPT_TYPE="qwen-boxed"
# 解析steps参数（支持格式：80 或 0,100,200 或 0-1000:200）
parse_steps() {
    local step_str=$1
    if [[ $step_str == *"-"* ]]; then
        # 处理范围格式 0-1000:200
        local range_part=${step_str%%:*}
        local interval=${step_str#*:}
        interval=${interval:-100}  # 默认间隔100
        
        local start=${range_part%-*}
        local end=${range_part#*-}
        seq $start $interval $end
    elif [[ $step_str == *,* ]]; then
        # 处理逗号分隔格式
        tr ',' '\n' <<< "$step_str"
    else
        # 单个数值
        echo "$step_str"
    fi
}
# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        --prompt_type)
        PROMPT_TYPE="$2"
        shift 2
        ;;
        --model_dir)
        MODEL_DIR="$2"
        shift 2
        ;;
        --steps)
        STEPS="$2"
        shift 2
        ;;
        --benchmarks)
        BENCHMARKS="$2"
        shift 2
        ;;
        *)
        echo "Unknown option: $1"
        exit 1
        ;;
    esac
done

# 解析steps参数函数保持不变...

# 生成步骤列表
STEPS_LIST=($(parse_steps "$STEPS"))

# 生成benchmark列表
IFS=',' read -ra BENCHMARK_LIST <<< "$BENCHMARKS"

# 执行所有组合
# for step in "${STEPS_LIST[@]}"; do
#     for benchmark in "${BENCHMARK_LIST[@]}"; do
#         # 修改文件名部分
#         INPUT_PATH="${MODEL_DIR}/global_step_${step}/actor/huggingface/math_eval/${benchmark}/test_${PROMPT_TYPE}_-1_seed0_t1.0_s0_e-1.jsonl"
        
#         if [[ -f "$INPUT_PATH" ]]; then
#             echo "Processing: step=${step} benchmark=${benchmark} prompt=${PROMPT_TYPE}"
#             python call_gpt.py --input_path "$INPUT_PATH"
#         else
#             echo "Warning: File not found - ${INPUT_PATH}"
#         fi
#     done
# done
for step in "${STEPS_LIST[@]}"; do
    for benchmark in "${BENCHMARK_LIST[@]}"; do
        # 原始路径构造
        INPUT_PATH="${MODEL_DIR}/global_step${step}/actor/huggingface/math_eval/${benchmark}/test_${PROMPT_TYPE}_-1_seed0_t0.0_s0_e-1.jsonl"
        
        # 路径回退逻辑
        if [[ ! -f "$INPUT_PATH" ]]; then
            # 构造备用路径（移除中间目录层级）
            FALLBACK_PATH="${MODEL_DIR}/global_step${step}/${benchmark}/test_${PROMPT_TYPE}_-1_seed0_t0.0_s0_e-1.jsonl"
            
            if [[ -f "$FALLBACK_PATH" ]]; then
                INPUT_PATH="$FALLBACK_PATH"
                echo "Notice: Using fallback path for step=${step} benchmark=${benchmark}"
            fi
        fi

        if [[ -f "$INPUT_PATH" ]]; then
            echo "Processing: step=${step} benchmark=${benchmark} prompt=${PROMPT_TYPE}"
            python call_gpt.py --input_path "$INPUT_PATH"
        else
            echo "Warning: File not found - ${INPUT_PATH}"
            # 显示备用路径供调试
            echo "Debug: Fallback path also missing - ${FALLBACK_PATH}"
        fi
    done
done
