#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dataset JSON creator for GeometrySegmentation.
生成される data.json の構造（例）:
{
    "0": [
        {
            "image": "case1/img.nii.gz",
            "label": "case1/lab.nii.gz",
            "verts": "case1/mesh.xyz"
        }
    ],
    "1": [
        {
            "image": "case2/img.nii.gz",
            "label": "case2/lab.nii.gz",
            "verts": "case2/mesh.xyz"
        }
    ],
    ...
}
"""

import os
import json
import re
from pathlib import Path

def make_dataset_json(root_dir: str = "/media/connect-to-vm/data/CoronaryArtery",
                      out_json: str = "data.json") -> None:
    """
    Parameters
    ----------
    root_dir : str
        ケースフォルダ (case1~case1000) が格納されているルートディレクトリ
    out_json : str
        出力する json ファイル名（ルート直下を想定）
    """
    root = Path(root_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"{root} が見つかりません")

    # case ディレクトリを数字順にソート
    case_dirs = sorted(
        [d for d in root.iterdir() if d.is_dir()],
        key=lambda x: int(re.sub(r"\D", "", x.name))
    )

    dataset = {}
    idx = 0
    for case_dir in case_dirs:
        img_path   = case_dir / "img.nii.gz"
        label_path = case_dir / "lab.nii.gz"
        mesh_path  = case_dir / "mesh.xyz"

        # 3ファイルがそろっているか確認
        if not (img_path.is_file() and label_path.is_file() and mesh_path.is_file()):
            print(f"[Warning] 必要ファイル欠如: {case_dir.name} をスキップ")
            continue

        # dataset.py 側で root_dir が付加されるので相対パスで記録する
        entry = {
            "image": f"{case_dir.name}/img.nii.gz",
            "label": f"{case_dir.name}/lab.nii.gz",
            "verts": f"{case_dir.name}/mesh.xyz"
        }
        dataset[str(idx)] = [entry]
        idx += 1

    # JSON 保存
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4)
    print(f"✅  {out_json} を出力しました（{len(dataset)} 件）")

if __name__ == "__main__":
    make_dataset_json()
