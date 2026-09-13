#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""adblock-hosts 的 sing-box rule-set (.srs) 生成器（便携、无第三方依赖）

输入 : domain/blacklist.txt, domain/whitelist.txt（与 build_dat.py 共用同一份权威清单）
输出 : singbox/Lhl-blacklist.srs, singbox/Lhl-whitelist.srs

匹配语义 : `domain`（**等值**匹配，只命中该确切域名、不含子域名）
           与 geodata/Lhl.dat 的 `full` 语义保持一致。

用法 :
  # 1) 指定 sing-box 二进制（推荐，本地编译；无需 CI）
  python3 .github/scripts/build_srs.py --sing-box /path/to/sing-box
  SING_BOX_BIN=/path/to/sing-box python3 .github/scripts/build_srs.py

  # 2) 仅生成源 JSON（不编译），供其它工具/人工检查
  python3 .github/scripts/build_srs.py --dump-json

  # 3) 生成源 JSON 并保留到 singbox/src/（默认只放临时目录，编译后丢弃）
  python3 .github/scripts/build_srs.py --sing-box /path/to/sing-box --keep-json

注 : .srs 是二进制格式，只能由 sing-box 官方二进制编译，本脚本不代构建；
     未找到 sing-box 时只生成源 JSON 并提示。
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUTDIR = os.path.join(ROOT, "singbox")
SRCDIR = os.path.join(OUTDIR, "src")

# (产物名, 源清单)
SETS = [
    ("Lhl-blacklist", os.path.join(ROOT, "domain", "blacklist.txt")),
    ("Lhl-whitelist", os.path.join(ROOT, "domain", "whitelist.txt")),
]


def clean(path):
    """读取清单：丢弃空行与 # 注释、去掉行内注释与首尾空白；保持顺序去重。"""
    out, seen = [], set()
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.rstrip("\r\n")
            if not ln or ln.startswith("#"):
                continue
            ln = ln.split("#")[0].strip()
            if ln and ln not in seen:
                seen.add(ln)
                out.append(ln)
    return out


def build_source(domains):
    """sing-box rule-set 源格式：等值 domain 匹配。"""
    return {"version": 1, "rules": [{"domain": list(domains)}]}


def find_sing_box(arg):
    """按 参数 -> $SING_BOX_BIN -> PATH 顺序找 sing-box 可执行文件。"""
    for cand in (arg, os.environ.get("SING_BOX_BIN")):
        if cand:
            if os.path.isfile(cand) and os.access(cand, os.X_OK):
                return cand
            found = shutil.which(cand)
            if found:
                return found
    return shutil.which("sing-box")


def main():
    ap = argparse.ArgumentParser(description="由 domain/*.txt 生成 sing-box .srs 规则集")
    ap.add_argument("--sing-box", default=None,
                    help="sing-box 可执行文件路径（缺省读 $SING_BOX_BIN 或 PATH）")
    ap.add_argument("--dump-json", action="store_true",
                    help="只生成源 JSON，不编译（输出到 singbox/src/）")
    ap.add_argument("--keep-json", action="store_true",
                    help="编译时也把源 JSON 保留到 singbox/src/")
    args = ap.parse_args()

    os.makedirs(OUTDIR, exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="lhl-srs-")
    exe = None if args.dump_json else find_sing_box(args.sing_box)

    rc = 0
    for name, src in SETS:
        if not os.path.isfile(src):
            print("[error] 缺少清单文件: %s" % src, file=sys.stderr)
            rc = 1
            continue

        domains = clean(src)
        json_path = os.path.join(tmpdir, name + ".json")
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(build_source(domains), fh, ensure_ascii=False, indent=2)
            fh.write("\n")

        if args.dump_json or not exe:
            os.makedirs(SRCDIR, exist_ok=True)
            kept = os.path.join(SRCDIR, name + ".json")
            shutil.copyfile(json_path, kept)
            print("%-16s %4d 条 -> %s" % (name, len(domains), os.path.relpath(kept, ROOT)))
            if not args.dump_json:
                print("  [提示] 未找到 sing-box，仅生成源 JSON；"
                      "用 --sing-box <路径> 或 SING_BOX_BIN=<路径> 可编译 .srs")
                rc = 1
            continue

        out_path = os.path.join(OUTDIR, name + ".srs")
        cmd = [exe, "rule-set", "compile", "--output", out_path, json_path]
        print("%-16s %4d 条 -> %s" % (name, len(domains), os.path.relpath(out_path, ROOT)))
        print("  $ " + " ".join(cmd[:1] + cmd[1:]))
        try:
            subprocess.check_call(cmd)
        except (OSError, subprocess.CalledProcessError) as exc:
            print("[error] 编译失败: %s" % exc, file=sys.stderr)
            rc = 1
            continue

        if args.keep_json:
            os.makedirs(SRCDIR, exist_ok=True)
            shutil.copyfile(json_path, os.path.join(SRCDIR, name + ".json"))

    shutil.rmtree(tmpdir, ignore_errors=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
