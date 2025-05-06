# bash call_gpt.sh \
#     --model_dir /cfs2/hadoop-aipnlp/zengweihao02/checkpoints/verl-grpo-llama3.1-8b-rollout-1024-256mini-remove-reward-tem1.0-fixv1-fix_abel_remove_gsm8k_level1_Llama-3.1-8B \
#     --steps "0,5,10,20,30,40,50,60,70,80" \
#     --benchmarks "olympiadbench,math500" \
#     --prompt_type abel \


# bash call_gpt.sh \
#     --model_dir /cfs2/hadoop-aipnlp/zengweihao02/checkpoints/verl-grpo-llama3.1-8b-rollout-1024-256mini-remove-reward-tem1.0-fixv1-fix_abel_remove_gsm8k_level1_Llama-3.1-8B \
#     --steps "0,5,10,20,30,40,50,60,70,80" \
#     --benchmarks "olympiadbench,math500" \
#     --prompt_type abel \



# bash call_gpt.sh \
#     --model_dir /cfs2/hadoop-aipnlp/zengweihao02/checkpoints/verl-grpo-mistral-7b-rollout-1024-256mini-remove-reward-tem1.0-fixv1-fix_abel_remove_gsm8k_level1_Mistral-7B-v0.1 \
#     --steps "0,5,10,20,30,40,50,60,70,80,90,100" \
#     --benchmarks "olympiadbench,math500" \
#     --prompt_type abel \


# bash call_gpt.sh \
#     --model_dir /cfs2/hadoop-aipnlp/zengweihao02/checkpoints/verl-grpo-mistral-7b-rollout-1024-256mini-remove-reward-tem1.0-fixv1-fix_abel_remove_level1to4_Mistral-7B-v0.1 \
#     --steps "0,5,10,20,30,40,50,60,70,80,90,100" \
#     --benchmarks "olympiadbench,math500" \
#     --prompt_type abel \


# bash call_gpt.sh \
#     --model_dir /cfs2/hadoop-aipnlp/zengweihao02/checkpoints/verl-grpo-llama3.1-8b-rollout-1024-256mini-remove-reward-tem1.0-fixv1-fix_abel_remove_level1to4_Llama-3.1-8B \
#     --steps "0,5,10,20,30,40,50,60,70,80,90,100" \
#     --benchmarks "olympiadbench,math500" \
#     --prompt_type abel \


# bash call_gpt.sh \
#     --model_dir /cfs2/hadoop-aipnlp/zengweihao02/checkpoints/verl-grpo-llama3.1-8b-rollout-1024-256mini-remove-reward-tem1.0-fixv1-fix_abel_remove_level3to5_Llama-3.1-8B \
#     --steps "0,5,10,20,30,40,50,60,70,80,90,100" \
#     --benchmarks "olympiadbench,math500" \
#     --prompt_type abel \


# bash call_gpt.sh \
#     --model_dir /cfs2/hadoop-aipnlp/zengweihao02/checkpoints/verl-grpo-deepseek-math-base-rollout-1024-256mini-remove-reward-tem1.0-fix_qwen_remove_level1to4_deepseek-math-7b-base \
#     --steps "0,5,10,20,30,40,50,60,70,80,90,100" \
#     --benchmarks "olympiadbench,math500" \
#     --prompt_type qwen-boxed \


# bash call_gpt.sh \
#     --model_dir /cfs2/hadoop-aipnlp/zengweihao02/checkpoints/verl-grpo-deepseek-math-base-rollout-1024-256mini-remove-reward-tem1.0-fix_qwen_remove_level3to5_deepseek-math-7b-base \
#     --steps "0,5,10,20,30,40,50,60,70,80,90,100" \
#     --benchmarks "olympiadbench,math500" \
#     --prompt_type qwen-boxed \


# bash call_gpt.sh \
#     --model_dir /cfs2/hadoop-aipnlp/zengweihao02/checkpoints/verl-grpo-llama3.1-8b-rollout-1024-256mini-remove-reward-tem1.0-fixv1-fix-fixv2_abel_remove_gsm8k_level1_Llama-3.1-8B \
#     --steps "0,5,10,20,30,40,50,60,70,80,90,100" \
#     --benchmarks "olympiadbench" \
#     --prompt_type abel \


# bash call_gpt.sh \
#     --model_dir /cfs/hadoop-aipnlp/zengweihao02/OpenRLHF/policy_scale/simplerl_data/simplerl_eval/verl-grpo-mistral-7b-rollout-1024-256mini-remove-reward-tem1.0-fixv1-fix_abel_remove_gsm8k_level1_Mistral-7B-v0.1 \
#     --steps "70,80,90,100" \
#     --benchmarks "olympiadbench" \
#     --prompt_type abel \


# bash call_gpt.sh \
#     --model_dir /cfs/hadoop-aipnlp/zengweihao02/OpenRLHF/policy_scale/simplerl_data/simplerl_eval/verl-grpo_Mistral-Small-24B-Base-2501_remove_clipFalse_max_response8192_batch1024_rollout8_klcoef0.001_entcoef0.001_simplelr_math_35_remove_format_reward_v1 \
#     --steps "0,5,10,20,30,40,50,60,70,80,90,100" \
#     --benchmarks "olympiadbench,math500" \
#     --prompt_type qwen-boxed \




bash call_gpt.sh \
    --model_dir /cfs/hadoop-aipnlp/zengweihao02/OpenRLHF/policy_scale/simplerl_data/simplerl_eval/Mistral-24B-numinamath-sft_v1 \
    --steps "100,500" \
    --benchmarks "aime24,amc23,math500,olympiadbench" \
    --prompt_type qwen-boxed \