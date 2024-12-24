# Stable Animator: 高质量 ID-Perserving 人物动漫化视频生成推理

## 1. 模型简介
StableAnimator是由姿势驱动的人体运动动画生成模型，展示了合成图像的高保真度和ID-perserving能力。动画可由StableAnimator直接合成，无需使用任何与面部相关的后处理工具。具体实现借鉴于[Francis-Rings/StableAnimator](https://github.com/Francis-Rings/StableAnimator/tree/main)

![](https://github.com/Francis-Rings/StableAnimator/raw/main/assets/figures/framework.jpg?raw=true)
![](https://github.com/Francis-Rings/StableAnimator/raw/main/assets/figures/case-18.gif?raw=true)

注：上图引自 [StableAnimator](https://arxiv.org/abs/2411.17697)。

## 2. 环境准备

通过 `git clone` 命令拉取 PaddleMIX 源码，并安装必要的依赖库。请确保你的 PaddlePaddle 框架版本在 2.6.0 之后，PaddlePaddle 框架安装可参考 [飞桨官网-安装](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/install/pip/linux-pip.html)。

```bash
# 克隆 PaddleMIX 仓库
git clone https://github.com/PaddlePaddle/PaddleMIX

# 可以查看 https://www.paddlepaddle.org.cn/ 寻找自己适合的版本
python -m pip install paddlepaddle-gpu==2.6.0.post120 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html

# 进入consistency_distillation目录
cd PaddleMIX/ppdiffusers/examples/StableAnimator/

# 安装新版本ppdiffusers
pip install https://paddlenlp.bj.bcebos.com/models/community/junnyu/wheels/ppdiffusers-0.24.0-py3-none-any.whl --user

# 安装其他所需的依赖, 如果提示权限不够，请在最后增加 --user 选项
pip install -r requirements.txt