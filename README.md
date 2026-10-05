# randpick

终端随机抽取 / 洗牌小工具：抽签、摇人、随机点名、打乱顺序。

纯标准库（`secrets` / `argparse` / `json`），零依赖，离线可用。

## 安装

```bash
cd randpick
python3 -m randpick --help
```

## 用法

```bash
randpick a b c                  # 抽 1 个
randpick a b c --count 2        # 抽 2 个（不放回）
randpick a b c --count 3 --with-replacement   # 放回抽取（可重复）
randpick --shuffle a b c        # 洗牌：输出全部候选的随机排列
randpick --file names.txt       # 从文件读候选（一行一个）
cat names.txt | randpick        # 管道读候选
randpick a b c --seed 42        # 确定性模式（演示/复现用）
randpick a b c --json           # JSON 输出
```

## 设计取舍

- **默认随机源是 `secrets.SystemRandom`**（CSPRNG），抽签场景够公平；
  `--seed` 切换到 `random.Random`，**只用于演示和复现**，别拿它做安全相关抽取。
- 这不是密钥/令牌生成器——要密码请用兄弟项目 `passgen`。
- `--count` 超过候选数（不放回）时明确报错，不静默截断。

## 已知局限

- `--seed` 的确定性只保证同版本 Python 同算法下的复现；
- 空输入（无参数、无文件、无管道）时中文报错，exit 1；
- `--shuffle` 不能与 `--count` / `--with-replacement` 同用。

## License

MIT，Copyright (c) 2026 ljiang9。
