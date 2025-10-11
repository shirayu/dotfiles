#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

# ----------------------------------------------------------------------
# 1. Dataclasses for Configuration
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class LinkConfig:
    """config.json の 'links' セクションの項目を保持します。"""

    source: str
    target: str
    all: bool = field(default=False)


@dataclass(frozen=True)
class DotfileConfig:
    """config.json 全体の設定を保持します。"""

    links: List[LinkConfig]
    deprecated: List[str] = field(default_factory=list)
    exist_files: List[str] = field(default_factory=list)
    exist_commands: List[str] = field(default_factory=list)


# ----------------------------------------------------------------------
# 2. Utility & Setup Functions
# ----------------------------------------------------------------------

# ホームディレクトリのパスをキャッシュ
HOME_DIR = Path.home()
CONFIG_FILE_NAME = "config.json"


def resolve_path(path_str: str) -> Path:
    """パス文字列内の '~' をホームディレクトリに展開し、Pathオブジェクトを返します。"""
    return Path(path_str.replace("~/", str(HOME_DIR) + os.sep))


def _load_config(config_path: Path) -> DotfileConfig:
    """設定ファイルを読み込み、DotfileConfig dataclass に変換します。"""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(
            f"エラー: 設定ファイル '{config_path}' が見つかりません。", file=sys.stderr
        )
        sys.exit(1)
    except json.JSONDecodeError:
        print(
            f"エラー: 設定ファイル '{config_path}' の形式が不正です。", file=sys.stderr
        )
        sys.exit(1)

    try:
        link_configs = [LinkConfig(**link_data) for link_data in data.get("links", [])]
    except TypeError as e:
        print(f"エラー: link 設定のフィールドが不正です: {e}", file=sys.stderr)
        sys.exit(1)

    return DotfileConfig(
        links=link_configs,
        deprecated=data.get("deprecated", []),
        exist_files=data.get("exist_files", []),
        exist_commands=data.get("exist_commands", []),
    )


def _remove_existing_target(target_path: Path, dry_run: bool, action: str):
    """既存ファイルを削除します (上書き/修正のため)。"""
    if not dry_run:
        try:
            if target_path.is_dir() and not target_path.is_symlink():
                shutil.rmtree(target_path)
                print(f"  🗑️ {action}のためディレクトリを削除: {target_path}")
            else:
                os.unlink(target_path)
                print(f"  🗑️ {action}のためファイル/リンクを削除: {target_path}")
        except Exception as e:
            # 削除に失敗した場合、致命的エラーとして停止
            print(f"  ❌ 削除失敗 '{target_path.name}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"  [DRY-RUN] {action}のため既存ターゲットを削除予定: {target_path}")


def _create_symlink_action(source_path: Path, target_path: Path, dry_run: bool):
    """シンボリックリンクを作成する共通ロジック。（絶対パスで作成）"""
    # ソースの絶対パスを取得
    absolute_source = os.fspath(source_path.resolve())

    if not dry_run:
        try:
            os.unlink(target_path)
        except Exception:
            pass

        try:
            # 絶対パスでリンクを作成
            os.symlink(absolute_source, target_path)
            print(f"  ✅ リンク作成: '{target_path}' -> '{absolute_source}' (絶対パス)")
        except Exception as e:
            # リンク作成に失敗した場合、致命的エラーとして停止
            print(f"  ❌ リンク作成失敗 '{target_path.name}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(
            f"  [DRY-RUN] リンク作成予定: '{target_path}' -> '{absolute_source}' (絶対パス)"
        )


def _process_link_item_single(
    source_path: Path,
    target_path: Path,
    dry_run: bool,
    all_mode: bool,
):
    """単一のシンボリックリンクを作成、または自動修正します。"""

    is_existing_dir_not_link = target_path.is_dir() and not target_path.is_symlink()

    # source: "bin", target: "~/.local/bin" のような、非-allモードでディレクトリ全体をリンクしようとするケース
    is_common_dir_link_ambiguity = (
        not all_mode
        and source_path.is_dir()
        and is_existing_dir_not_link
        and target_path.name == source_path.name
    )

    # 既存のリンクが存在するか、かつ不正なリンクかをチェック
    is_broken_link = False
    if target_path.is_symlink():
        # resolve(strict=False) は、リンクが切れていてもパスを解決しようとする
        # resolve() は、リンクが切れていると FileNotFoundError を出すため、このチェックはより正確
        if target_path.resolve(strict=False) != source_path.resolve():
            is_broken_link = True

    # --- ターゲットの状況を判定 ---
    if not target_path.exists():
        status = "MISSING"
    elif target_path.is_symlink() and not is_broken_link:
        status = "CORRECT"
    elif is_broken_link:
        status = "BROKEN"
    elif is_common_dir_link_ambiguity:
        status = "AMBIGUOUS_DIR"
    else:
        status = "CONFLICT"

    # --- Run/Dry-Run Mode: 実行またはシミュレーション ---

    # 処理の分岐
    if status == "CORRECT":
        return  # 既に正しいリンク

    if status == "AMBIGUOUS_DIR":
        print(
            f"  - 既存ディレクトリ: '{target_path}' は実体ディレクトリです。リンクは作成せずスキップします。"
        )
        return  # スキップ

    # ターゲットの親ディレクトリが存在しない場合は作成
    if not target_path.parent.exists():
        if not dry_run:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"  - 親ディレクトリ '{target_path.parent}/' を作成しました。")
        else:
            print(f"  [DRY-RUN] 親ディレクトリ作成予定: '{target_path.parent}/'")

    if status == "MISSING":
        # リンクを作成する
        _create_symlink_action(source_path, target_path, dry_run)

    elif status == "BROKEN":
        # 不正なリンクを削除し、修正 (上書き)
        print(f"  🔄 不正なリンク '{target_path}' を修正します...")
        _remove_existing_target(target_path, dry_run, action="リンク修正")

        # 🚨 削除後の安全チェックを追加
        if not dry_run and target_path.exists():
            print(
                f"  ❌ 致命的エラー: ターゲット '{target_path}' が削除後も残っています。続行できません。",
                file=sys.stderr,
            )
            sys.exit(1)

        _create_symlink_action(source_path, target_path, dry_run)

    elif status == "CONFLICT":
        # 実体ファイル/ディレクトリを削除し、上書き
        print(f"  ⚠️ 競合ファイル '{target_path}' を上書きします...")
        _remove_existing_target(target_path, dry_run, action="上書き")

        # 🚨 削除後の安全チェックを追加
        if not dry_run and target_path.exists():
            print(
                f"  ❌ 致命的エラー: ターゲット '{target_path}' が削除後も残っています。続行できません。",
                file=sys.stderr,
            )
            sys.exit(1)

        _create_symlink_action(source_path, target_path, dry_run)


def _process_link_config(link_conf: LinkConfig, base_dir: Path, dry_run: bool):
    """LinkConfig の設定一つ分 (source/target) を処理します。"""
    source_name = link_conf.source.strip()
    target_template = link_conf.target.strip()

    target_template_path = resolve_path(target_template)
    if str(source_name).startswith("/") or str(source_name).startswith("~"):
        source_path = resolve_path(source_name)
    else:
        source_path = base_dir / source_name

    print(
        f"\n--- 処理中: source='{source_name}', target='{target_template}' ({'ALL' if link_conf.all else 'SINGLE'}) ---"
    )

    if not source_path.exists():
        print(f"警告: ソース '{source_name}' が存在しません。スキップします。")
        return

    if link_conf.all:
        if not source_path.is_dir():
            print(
                f"警告: 'all: true' ですが、ソース '{source_name}' はディレクトリではありません。スキップ。"
            )
            return

        # ディレクトリ直下の全ファイルを対象
        for item in source_path.iterdir():
            target_path = target_template_path / item.name
            _process_link_item_single(item, target_path, dry_run, True)
    else:
        # 修正されたロジック: SINGLEモード

        # target がディレクトリ終端であれば、source の「最終的な名前」をターゲットに付加する
        if target_template.endswith(("/", os.sep)):
            # source_path.name は 'home_config/.tmux.conf' の場合は '.tmux.conf' になる
            target_path = target_template_path / source_path.name
        else:
            target_path = target_template_path

        _process_link_item_single(source_path, target_path, dry_run, False)


# ----------------------------------------------------------------------
# 4. Main Operations
# ----------------------------------------------------------------------


def run_symlink_process(config: DotfileConfig, base_dir: Path, dry_run: bool):
    """全てのシンボリックリンクの作成、またはシミュレーションを行います。"""

    if dry_run:
        print(
            "## 🧪 ドライランモード: 実行内容をシミュレーションします。ファイルシステムは変更されません。"
        )
    else:
        print(
            "## 🔗 リンク作成モード: シンボリックリンクの作成を開始します。競合ファイル/不正リンクは自動的に上書き・修正されます。"
        )

    for link_conf in config.links:
        _process_link_config(link_conf, base_dir, dry_run)

    print("\n## 🏁 リンク処理が完了しました。")


def handle_deprecated(config: DotfileConfig) -> bool:
    """非推奨ファイルをチェックし、手動での削除を促します。（削除ロジックは含まない）"""
    if not config.deprecated:
        print("\n## 🗑️ 非推奨ファイルの処理: 対象なし")
        return True

    print("\n## 🗑️ 非推奨ファイルの確認を開始します...")

    deprecated_found = []

    for item in config.deprecated:
        item_path = resolve_path(item)

        # 存在確認 (ファイル/リンクのどちらも)
        if item_path.exists() or item_path.is_symlink():
            print(f"  [DETECTED] 存在します: '{item_path}'")
            deprecated_found.append(item_path)

    if deprecated_found:
        print("\n### 🚨 以下の非推奨ファイル/リンクが検出されました。")
        print(
            "これらは設定から削除対象としてマークされていますが、まだ存在しています。"
        )
        print("➡️ **手動で削除してください。**")

        for path in deprecated_found:
            print(f"  - {path}")

    print("\n## 🏁 非推奨ファイルの確認が完了しました。")
    return len(deprecated_found) == 0


def handle_exists(config: DotfileConfig) -> bool:
    """必須のパスが存在するかをチェックします。"""
    if not config.exist_commands:
        print("\n## 🔎 必須ファイルの確認: 対象なし")
        return True

    print("\n## 🔎 必須ファイルの確認を開始します...")

    missing_paths = []
    all_exist = True

    for item in config.exist_files:
        item_path = resolve_path(item)

        if not item_path.exists():
            print(f"  [MISSING] 🚨 存在しません: '{item}'")
            missing_paths.append(item)
            all_exist = False
        else:
            print(f"  [OK] 存在します: '{item}'")

    if not all_exist:
        print("\n### 🚨 以下の必須ファイル/ディレクトリが見つかりませんでした。")
        print("➡️ **手動で作成またはインストールしてください。**")
        for item in missing_paths:
            print(f"  - {item}")
        return False
    else:
        print("\n## 🏁 必須ファイルの確認が完了しました。全て存在します。")
        return True


def check_commands_exist(config: DotfileConfig) -> bool:
    """
    設定されたコマンド群の中から、実行可能ファイルとして存在しないものをチェックします。
    コマンドの実行ではなく、存在チェックを行います。（whichコマンド相当）
    """
    if not config.exist_commands:
        print("\n## ⚙️ 外部コマンドの存在確認: 対象なし")
        return True

    print("\n## ⚙️ 外部コマンドの存在確認を開始します...")

    missing_commands = []
    all_exist = True

    for full_command in config.exist_commands:
        # コマンドの先頭部分（実行ファイル名）のみを取得
        # 例: "git submodule update" -> "git"
        command_name = full_command.split()[0]

        try:
            # shutil.which は、OSのPATHから実行可能ファイルを探す
            if shutil.which(command_name):
                print(f"  [OK] 存在します: '{command_name}' (実行: '{full_command}')")
            else:
                print(
                    f"  [MISSING] 🚨 見つかりません: '{command_name}' (実行: '{full_command}')"
                )
                missing_commands.append(command_name)
                all_exist = False
        except Exception:
            # 予期せぬエラー (稀だが)
            print(f"  [ERROR] 🚨 確認中にエラーが発生: '{command_name}'")
            missing_commands.append(command_name)
            all_exist = False

    if not all_exist:
        print("\n### 🚨 以下のコマンド実行ファイルが見つかりませんでした。")
        print("➡️ **PATHに追加されているか、手動でインストールしてください。**")
        for name in missing_commands:
            print(f"  - {name}")
        print()
        print(f"=> sudo apt install {' '.join(missing_commands)}")
        return False

    print("\n## 🏁 外部コマンドの存在確認が完了しました。")
    return True


# ----------------------------------------------------------------------
# 5. Main Execution
# ----------------------------------------------------------------------


def main():
    """argparse を使用したメイン処理を実行します。"""
    parser = argparse.ArgumentParser(
        description="ドットファイル管理スクリプト (シンボリックリンク作成/ドライラン)",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=CONFIG_FILE_NAME,
        help=f"設定ファイル名 (デフォルト: {CONFIG_FILE_NAME})",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="ファイルシステムを変更せず、実行する操作をシミュレーションします。",
    )

    args = parser.parse_args()
    ok: bool = True

    # スクリプトの実行ディレクトリをドットファイルのベースとする
    base_dir = Path.cwd()
    config = _load_config(Path(args.config))

    dry_run_mode = args.dry_run

    print(f"ドットファイルベースディレクトリ: {base_dir}")
    print(f"ホームディレクトリ: {HOME_DIR}\n")

    # 1. シンボリックリンクの処理 (作成/シミュレーション)
    run_symlink_process(config, base_dir, dry_run_mode)

    # 2. 非推奨ファイルの確認 (削除は手動)
    ok = ok and handle_deprecated(config)

    # 3. 必須ファイルの存在確認
    ok = ok and handle_exists(config)

    # 4. 外部コマンドの実行ファイル存在確認
    ok = ok and check_commands_exist(config)

    print("\n✅ 全ての処理が完了しました。")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n処理を中断しました。", file=sys.stderr)
        sys.exit(1)
