# Stable Animator: 高质量 ID-Perserving 人物动漫化视频生成推理
## 1. 模型简介
StableAnimator是由姿势驱动的人体运动动画生成模型，展示了合成图像的高保真度和ID-perserving能力。动画可由StableAnimator直接合成，无需使用任何与面部相关的后处理工具。具体实现借鉴于[Francis-Rings/StableAnimator](https://github.com/Francis-Rings/StableAnimator/tree/main)

目前用于人物图像动画的扩散模型难以确保身份（ID）的一致性。StableAnimator，这是第一个端到端的ID保持视频扩散框架，它在参考图像和姿势的条件下，无需任何后处理即可合成高质量的视频。StableAnimator包含精心设计的模块，用于训练和推理，努力实现身份一致性。首先，StableAnimator使用现成的提取器计算image-embedding和face-embdeing。然后，StableAnimator引入了一种新的分布感知ID-adapter，该adepter可以防止时间层引起的干扰，同时通过对齐来保留ID。在推理过程中，StableAnimator提出基于Hamilton-Jacobi-Bellman（HJB）方程的优化方法，以进一步提高人脸质量。


![](https://github.com/Francis-Rings/StableAnimator/raw/main/assets/figures/framework.jpg?raw=true)
![](https://github.com/Francis-Rings/StableAnimator/raw/main/assets/figures/case-18.gif?raw=true)

注：上图引自 [StableAnimator](https://arxiv.org/abs/2411.17697)。
## 2. 环境准备
通过 `git clone` 命令拉取 PaddleMIX 源码，并安装必要的依赖库。请确保你的 PaddlePaddle 框架版本在 2.6.0 之后，PaddlePaddle 框架安装可参考 [飞桨官网-安装](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/install/pip/linux-pip.html)。
```bash
# 克隆 PaddleMIX 仓库
git clone https://github.com/PaddlePaddle/PaddleMIX

# 安装2.6.0版本的paddlepaddle-gpu，当前我们选择了cuda12.0的版本，可以查看 https://www.paddlepaddle.org.cn/ 寻找自己适合的版本
python -m pip install paddlepaddle-gpu==2.6.0.post120 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html

# 进入consistency_distillation目录
cd PaddleMIX/ppdiffusers/examples/InstantID/

# 安装新版本ppdiffusers
pip install https://paddlenlp.bj.bcebos.com/models/community/junnyu/wheels/ppdiffusers-0.24.0-py3-none-any.whl --user

# 安装其他所需的依赖, 如果提示权限不够，请在最后增加 --user 选项
pip install -r requirements.txt
```

## 3. 数据准备

测试样例需要按照以下格式排列：
inference/
├── case-1
│   ├── poses
│   ├── faces
│   └── reference.png
├── case-2
│   ├── poses
│   ├── faces
│   └── reference.png
├── case-3
│   ├── poses
│   ├── faces
│   └── reference.png

poses文件夹包含所有姿势图像，faces文件夹包含所有面部图像，reference.png是参考图像。

### 姿态图提取
我们利用预训练的DWPose来提取人体骨骼。在初始化DWPose时，应在中配置预训练权重。
给定包含多个.png文件的目标图像文件夹，您可以使用命令获取相应的人体姿态图。
需要注意的是，target文件夹中的.png文件以frame_i.png格式命名，如frame_0.png、frame_1.png等。--ref_image_path表示给定参考图像的路径。获得的人体姿态图像保存在path/test/pose中。特别重要的是，inference姿态图像应该与关于身体形状的参考图像对齐。
如果您只有目标MP4文件，我们建议您使用ffmpeg将MP4文件转换为多帧（.png文件），而不会造成任何质量损失。

### 面部图提取
给定包含多个RGB.png文件的图像文件夹的路径，您可以运行以下命令来提取相应的人脸mask。

StableAnimator支持两种不同分辨率设置的人体图像动画：512x512和576x1024。您可以在command_basic_infer.sh中修改“--width”和“--height”来设置动画的分辨率。