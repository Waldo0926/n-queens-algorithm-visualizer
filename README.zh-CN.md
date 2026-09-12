# N 皇后算法可视化与对比 ♛

这是一个整理后的 Python 算法项目，用三种不同方法解决并比较 **N-Queens / N 皇后问题**：

- **回溯法（Backtracking）**：DFS + 行/对角线约束检查；
- **剪枝状态空间搜索（Pruned state-space search）**：把棋盘编码为 N 进制状态，发现冲突前缀后直接跳过一批无效状态；
- **爬山法（Hill Climbing）**：基于冲突数量进行局部搜索，并支持随机重启。

本仓库由早期《算法设计与分析》课程设计重新整理而来。公开版没有直接保留原始作业目录，而是重新组织成更适合 GitHub 展示、复现和面试讲解的工程结构。

## 快速运行

需要 Python 3.10+。核心算法只使用 Python 标准库。

```bash
python main.py solve --algorithm backtracking --n 8
```

三种算法快速对比：

```bash
python main.py compare --n 8
```

枚举经典八皇后的全部 92 个解：

```bash
python main.py solve --algorithm backtracking --n 8 --all
```

爬山法（固定随机种子 + 最多 100 次随机重启）：

```bash
python main.py solve --algorithm hill-climbing --n 8 --seed 42 --restarts 100
```

启动图形界面：

```bash
python main.py visualize
```

## 这个项目展示了什么？

它不只是“八皇后作业”，而是用同一个问题展示三类典型算法思想：

1. **系统搜索**：递归、DFS、回溯；
2. **搜索空间剪枝**：利用第一个冲突位置跳过无效状态区间；
3. **启发式局部搜索**：用冲突数作为评价函数，同时展示 local minimum（局部最优）问题。

详细分析见 [docs/algorithm-analysis.md](docs/algorithm-analysis.md)。

## Benchmark

```bash
python benchmarks/benchmark.py --n 4 5 6 7 8 9 --hill-trials 100
```

脚本会生成 `benchmark_results.csv`，记录不同 N 下的成功率、工作量指标和运行时间。

## 自动测试

```bash
python -m unittest discover -s tests -p "test_*.py"
```

测试内容包括：

- 已知合法棋盘；
- 回溯法求解 N=8；
- N=8 的经典 **92 个解**；
- 状态空间剪枝确实减少枚举；
- 固定随机种子的爬山法 + 随机重启可得到合法解。

## 为什么没有把原压缩包直接放上来？

原始课程目录中包括虚拟环境、IDE 配置、多个实验草稿、绝对本地路径、Windows 专用 GUI 配置和学生信息。公开 GitHub 版本已经删除这些内容，并重新拆分为独立算法模块、CLI、GUI、测试与 benchmark，使它更像一个可维护的软件项目，而不是课程作业备份。
