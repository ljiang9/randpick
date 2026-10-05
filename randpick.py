#!/usr/bin/env python3
"""randpick —— 终端随机抽取 / 洗牌工具。

- 默认用 secrets（CSPRNG），适合抽签、摇人、随机点名；
- --seed 进入确定性模式（random.Random），只用于演示/复现；
- 不是密码学密钥材料生成器——要密钥请用兄弟项目 passgen。
"""
import argparse
import json
import random
import secrets
import sys

VERSION = "0.1.0"


def read_items(args):
    items = list(args.items)
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                items += [ln.strip() for ln in f if ln.strip()]
        except OSError as e:
            print(f"error: 无法读取文件 {args.file}：{e}", file=sys.stderr)
            sys.exit(2)
    if args.stdin or (not sys.stdin.isatty() and not args.items and not args.file):
        items += [ln.strip() for ln in sys.stdin if ln.strip()]
    if not items:
        print("error: 没有可抽取的候选项。请给出参数、--file 或用管道传入。", file=sys.stderr)
        sys.exit(1)
    return items


def make_rng(seed):
    if seed is not None:
        return random.Random(seed)
    return secrets.SystemRandom()


def cmd_pick(args):
    items = read_items(args)
    rng = make_rng(args.seed)
    n = args.count or 1
    if args.with_replacement:
        picks = [rng.choice(items) for _ in range(n)]
    else:
        if n > len(items):
            print(f"error: 要抽 {n} 个，但候选只有 {len(items)} 个（不放回）。", file=sys.stderr)
            sys.exit(1)
        picks = rng.sample(items, n)
    emit(picks, args)


def cmd_shuffle(args):
    items = read_items(args)
    rng = make_rng(args.seed)
    out = list(items)
    rng.shuffle(out)
    emit(out, args)


def emit(picks, args):
    if args.json:
        print(json.dumps({"picks": picks}, ensure_ascii=False))
    else:
        for p in picks:
            print(p)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="randpick",
        description="终端随机抽取：randpick a b c 抽一个；--shuffle 洗牌；--seed 演示复现。",
    )
    ap.add_argument("--version", action="version", version=f"randpick {VERSION}")
    ap.add_argument("items", nargs="*", help="候选项")
    ap.add_argument("--count", type=int, default=None, help="抽取个数（默认 1，不放回）")
    ap.add_argument("--with-replacement", action="store_true", help="放回抽取（可重复）")
    ap.add_argument("--shuffle", action="store_true", help="洗牌：输出全部候选的随机排列")
    ap.add_argument("--file", help="从文件读候选（一行一个）")
    ap.add_argument("--stdin", action="store_true", help="从 stdin 读候选")
    ap.add_argument("--seed", type=int, default=None, help="确定性种子（演示/复现用）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args(argv)

    if args.count is not None and args.count < 1:
        print("error: --count 必须 >= 1。", file=sys.stderr)
        sys.exit(2)
    if args.shuffle and (args.count is not None or args.with_replacement):
        print("error: --shuffle 不能与 --count/--with-replacement 同用。", file=sys.stderr)
        sys.exit(2)
    if args.shuffle:
        cmd_shuffle(args)
    else:
        cmd_pick(args)


if __name__ == "__main__":
    main()
