import argparse
import csv
import subprocess
import sys
from pathlib import Path

DOTFILE_PATHS = {}
with open("dots.csv", "r") as f:
    for row in csv.DictReader(f):
        DOTFILE_PATHS[row["Name"]] = (row["System"], row["Repo"])

SYSTEM_PATH = 0
REPO_PATH = 1


class DotfileManager:
    def __init__(self, config: dict[str, tuple], dry_run: bool = False):
        self.script_dir = Path(__file__).parent.absolute()
        self.config = self._expand_paths(config)
        self.dry_run = dry_run

    def _expand_paths(self, config: dict[str, tuple]) -> dict[str, tuple]:
        expanded = {}
        for name, paths in config.items():
            expanded[name] = (
                Path(paths[SYSTEM_PATH]).expanduser().resolve(),
                self.script_dir / paths[REPO_PATH].lstrip("./")
            )
        return expanded

    def _confirm_operation(self, message: str) -> bool:
        if self.dry_run:
            return True

        while True:
            response = input(f"{message} [y/N]: ").lower().strip()
            if response in ["y", "yes"]:
                return True
            elif response in ["n", "no", ""]:
                return False
            else:
                print("Please enter 'y' or 'n'")

    def _run_rsync(self, source: Path, dest: Path, name: str, delete_extra: bool = False) -> bool:
        # Create destination parent directory if it doesn't exist
        if not self.dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)

        rsync_args = ["rsync", "-avh", "--progress"]

        if delete_extra:
            rsync_args.append("--delete")

        if self.dry_run:
            rsync_args.append("--dry-run")

        # Ensure proper trailing slash handling for directories
        source_str = str(source).rstrip("/") + "/"
        dest_str = str(dest).rstrip("/") + "/"

        rsync_args.extend([source_str, dest_str])

        print(f"{name}: {source} -> {dest}")
        if delete_extra:
            print("  WARNING: Files in destination not present in source will be DELETED")
        if self.dry_run:
            print("  [DRY RUN - no changes will be made]")

        try:
            result = subprocess.run(
                rsync_args, check=True, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            if e.stderr:
                print(f"stderr: {e.stderr}")
            return False
        except FileNotFoundError:
            print("Error: rsync not found. Please install rsync.")
            return False

    def deploy(self, dotfiles: list[str] | None = None) -> bool:
        print("Deploying dotfiles from repository to system...")

        target_dotfiles = dotfiles if dotfiles else list(self.config.keys())

        print("\nFiles to deploy:")
        for name in target_dotfiles:
            if name not in self.config:
                print(f"  WARNING: '{name}' not found in configuration")
                continue
            paths = self.config[name]
            print(f"  {name}: {paths[REPO_PATH]} -> {paths[SYSTEM_PATH]}")

        if not self._confirm_operation("\nProceed with deployment?"):
            print("Deployment cancelled.")
            return False

        success = True

        for name in target_dotfiles:
            if name not in self.config:
                continue

            paths = self.config[name]

            if not paths[REPO_PATH].exists():
                print(
                    f"Warning: Repository directory {paths[REPO_PATH]} doesn't exist, skipping {name}")
                continue

            if not self._run_rsync(paths[REPO_PATH], paths[SYSTEM_PATH], f"Deploying {name}", delete_extra=True):
                success = False

        return success

    def retrieve(self, dotfiles: list[str] | None = None) -> bool:
        print("Retrieving dotfiles from system to repository...")

        target_dotfiles = dotfiles if dotfiles else list(self.config.keys())

        print("\nFiles to retrieve:")
        warnings = []
        for name in target_dotfiles:
            if name not in self.config:
                print(f"  WARNING: '{name}' not found in configuration")
                continue
            paths = self.config[name]

            # Safety check: warn if system doesn't exist but repo does
            if not paths[SYSTEM_PATH].exists():
                if paths[REPO_PATH].exists():
                    warnings.append(
                        f"  DANGER: {name} - System directory missing but repo has content!")
                    print(
                        f"  {name}: {paths[SYSTEM_PATH]} -> {paths[REPO_PATH]} (SYSTEM MISSING - WOULD DELETE REPO CONTENT)")
                else:
                    print(
                        f"  {name}: {paths[SYSTEM_PATH]} -> {paths[REPO_PATH]} (both missing)")
            else:
                print(f"  {name}: {paths[SYSTEM_PATH]} -> {paths[REPO_PATH]}")

        if warnings:
            print("\nDANGER WARNINGS:")
            for warning in warnings:
                print(warning)
            print("These operations would DELETE your repository content!")

        if not self._confirm_operation("\nProceed with retrieval?"):
            print("Retrieval cancelled.")
            return False

        success = True

        for name in target_dotfiles:
            if name not in self.config:
                continue

            paths = self.config[name]

            if not paths[SYSTEM_PATH].exists():
                # Extra safety: skip if system doesn't exist and repo does
                if paths[REPO_PATH].exists():
                    print(
                        f"SKIPPING {name}: System directory doesn't exist but repo has content - preserving repo")
                    continue
                else:
                    print(
                        f"Warning: System directory {paths[SYSTEM_PATH]} doesn't exist, skipping {name}")
                    continue

            if not self._run_rsync(paths[SYSTEM_PATH], paths[REPO_PATH], f"Retrieving {name}", delete_extra=True):
                success = False

        return success

    def create_backup(self, dotfiles: list[str] | None = None) -> bool:
        print("Creating backups of system files...")

        target_dotfiles = dotfiles if dotfiles else list(self.config.keys())

        print("\nFiles to backup:")
        for name in target_dotfiles:
            if name not in self.config:
                print(f"  WARNING: '{name}' not found in configuration")
                continue
            paths = self.config[name]
            backup_path = Path(str(paths[SYSTEM_PATH]) + ".bak")
            print(f"  {name}: {paths[SYSTEM_PATH]} -> {backup_path}")

        if not self._confirm_operation("\nProceed with backup creation?"):
            print("Backup cancelled.")
            return False

        success = True

        for name in target_dotfiles:
            if name not in self.config:
                continue

            paths = self.config[name]
            system_path = paths[SYSTEM_PATH]
            backup_path = Path(str(system_path) + ".bak")

            if not system_path.exists():
                print(
                    f"Warning: System directory {system_path} doesn't exist, skipping {name}")
                continue

            if backup_path.exists() and not self.dry_run:
                print(
                    f"Warning: Backup {backup_path} already exists, skipping {name}")
                continue

            if not self._run_rsync(system_path, backup_path, f"Backing up {name}"):
                success = False

        return success

    def restore_backup(self, dotfiles: list[str] | None = None) -> bool:
        print("Restoring from backup files...")

        target_dotfiles = dotfiles if dotfiles else list(self.config.keys())

        print("\nFiles to restore:")
        for name in target_dotfiles:
            if name not in self.config:
                print(f"  WARNING: '{name}' not found in configuration")
                continue
            paths = self.config[name]
            backup_path = Path(str(paths[SYSTEM_PATH]) + ".bak")
            print(f"  {name}: {backup_path} -> {paths[SYSTEM_PATH]}")

        if not self._confirm_operation("\nProceed with restore?"):
            print("Restore cancelled.")
            return False

        success = True

        for name in target_dotfiles:
            if name not in self.config:
                continue

            paths = self.config[name]
            system_path = paths[SYSTEM_PATH]
            backup_path = Path(str(system_path) + ".bak")

            if not backup_path.exists():
                print(
                    f"Warning: Backup file {backup_path} doesn't exist, skipping {name}")
                continue

            if not self._run_rsync(backup_path, system_path, f"Restoring {name}", delete_extra=True):
                success = False

        return success

    def delete_backup(self, dotfiles: list[str] | None = None) -> bool:
        print("Deleting backup files...")

        target_dotfiles = dotfiles if dotfiles else list(self.config.keys())

        print("\nBackup files to delete:")
        backups_to_delete = []
        for name in target_dotfiles:
            if name not in self.config:
                print(f"  WARNING: '{name}' not found in configuration")
                continue
            paths = self.config[name]
            backup_path = Path(str(paths[SYSTEM_PATH]) + ".bak")
            if backup_path.exists():
                print(f"  {name}: {backup_path}")
                backups_to_delete.append((name, backup_path))
            else:
                print(f"  {name}: {backup_path} (does not exist)")

        if not backups_to_delete:
            print("No backup files found to delete.")
            return True

        if not self._confirm_operation("\nProceed with backup deletion?"):
            print("Backup deletion cancelled.")
            return False

        success = True

        for name, backup_path in backups_to_delete:
            if self.dry_run:
                print(f"[DRY RUN] Would delete backup: {backup_path}")
                continue

            try:
                if backup_path.is_dir():
                    subprocess.run(["rm", "-rf", str(backup_path)], check=True)
                else:
                    backup_path.unlink()
                print(f"Deleted backup: {backup_path}")
            except (subprocess.CalledProcessError, OSError) as e:
                print(f"Error deleting {backup_path}: {e}")
                success = False

        return success

    def list_dotfiles(self):
        print("Configured dotfiles:")
        for name, paths in self.config.items():
            system_exists = "EXISTS" if paths[SYSTEM_PATH].exists() else "MISSING"
            repo_exists = "EXISTS" if paths[REPO_PATH].exists() else "MISSING"

            print(f"  {name}:")
            print(f"    System: {paths[SYSTEM_PATH]} ({system_exists})")
            print(f"    Repo:   {paths[REPO_PATH]} ({repo_exists})")
            print()

    def diff(self, dotfiles: list[str] | None = None):
        target_dotfiles = dotfiles if dotfiles else list(self.config.keys())

        # Validate input
        for name in target_dotfiles:
            if name not in self.config:
                print(f"  WARNING: '{name}' not found in configuration")
                continue

            paths = self.config[name]

            # Check if both sides exist
            match (paths[REPO_PATH].exists(), paths[SYSTEM_PATH].exists()):
                case (False, False):
                    print(
                        f"{name} does not exist either in the repo or on the system")
                    continue
                case (False, True):
                    print(f"{name} does not exist in the repo")
                    continue
                case (True, False):
                    print(f"{name} does not exist on the system")
                    continue

            subprocess.run(
                f"diff -ru {paths[REPO_PATH]} {paths[SYSTEM_PATH]} | diff-so-fancy", text=True, shell=True, check=True)


def interactive_menu():
    while True:
        print("\nDotfiles Manager - Interactive Mode")
        print("===================================")
        print("d. Deploy (repo -> system)")
        print("r. Retrieve (system -> repo)")
        print("b. Create backup")
        print("R. Restore backup")
        print("D. Delete backup")
        print("l. List dotfiles")
        print("f. Show the difference (repo - system)")
        print("q. Exit")

        try:
            choice = input("\nSelect operation: ").strip()

            if choice == "q":
                print("Goodbye!")
                break
            elif choice in ["d", "r", "b", "R", "D", "f"]:
                # Show available dotfiles
                print(
                    f"\nAvailable dotfiles: {', '.join(DOTFILE_PATHS.keys())}")
                selection = input(
                    "Enter dotfile names (space-separated, or press Enter for all): ").strip()
                dotfiles = selection.split() if selection else None

                if dotfiles:
                    invalid = set(dotfiles) - set(DOTFILE_PATHS.keys())
                    if invalid:
                        print(f"Error: Unknown dotfiles: {', '.join(invalid)}")
                        continue

                # Only ask about dry run if it's applicable
                if choice in ["d", "r", "b", "R", "D"]:
                    dry_run = input(
                        "Dry run? [y/N]: ").lower().strip() in ["y", "yes"]
                else:
                    dry_run = False

                manager = DotfileManager(DOTFILE_PATHS, dry_run=dry_run)

                match choice:
                    case "d":
                        manager.deploy(dotfiles)
                    case "r":
                        manager.retrieve(dotfiles)
                    case "b":
                        manager.create_backup(dotfiles)
                    case "R":
                        manager.restore_backup(dotfiles)
                    case "D":
                        manager.delete_backup(dotfiles)
                    case "f":
                        manager.diff(dotfiles)

            elif choice == "l":
                manager = DotfileManager(DOTFILE_PATHS)
                manager.list_dotfiles()
            else:
                print("Invalid choice.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Dotfiles Manager - Sync configuration files between system and repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --deploy                    Deploy all dotfiles to system
    %(prog)s --deploy nvim fish          Deploy specific dotfiles
    %(prog)s --retrieve nvim             Retrieve specific dotfiles
    %(prog)s --backup --dry-run          Preview backup creation
    %(prog)s --restore --delete-backup   Restore and clean up backups
        """
    )

    # Main operations
    parser.add_argument(
        "-d", "--deploy",
        action="store_true",
        help="Deploy dotfiles from repository to system"
    )
    parser.add_argument(
        "-r", "--retrieve",
        action="store_true",
        help="Retrieve dotfiles from system to repository"
    )

    # Backup operations
    parser.add_argument(
        "-b", "--backup",
        action="store_true",
        help="Create backup copies of system files"
    )
    parser.add_argument(
        "-R", "--restore",
        action="store_true",
        help="Restore files from backup copies"
    )
    parser.add_argument(
        "-D", "--delete-backup",
        action="store_true",
        help="Delete backup files"
    )

    # Utility operations
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all configured dotfiles"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "-f", "--diff",
        action="store_true",
        help="Show the difference between the repo and system versions of dotfiles"
    )

    # Target specific dotfiles
    parser.add_argument(
        "dotfiles",
        nargs="*",
        help="Specific dotfiles to operate on (default: all)"
    )

    return parser


def main():
    parser = create_argument_parser()

    # If no arguments, show interactive menu
    if len(sys.argv) == 1:
        interactive_menu()
        return

    args = parser.parse_args()

    # Initialize dotfile manager
    manager = DotfileManager(DOTFILE_PATHS, dry_run=args.dry_run)

    # Handle list and diff operations first
    if args.list:
        manager.list_dotfiles()
        return

    if args.diff:
        manager.diff(args.dotfiles)
        return

    # Validate dotfile names if specified
    if args.dotfiles:
        invalid_dotfiles = set(args.dotfiles) - set(DOTFILE_PATHS.keys())
        if invalid_dotfiles:
            print(f"Error: Unknown dotfiles: {', '.join(invalid_dotfiles)}")
            print(f"Available: {', '.join(DOTFILE_PATHS.keys())}")
            sys.exit(1)

    # Execute operations
    success = True

    if args.backup:
        success &= manager.create_backup(args.dotfiles)

    if args.deploy:
        success &= manager.deploy(args.dotfiles)

    if args.retrieve:
        success &= manager.retrieve(args.dotfiles)

    if args.restore:
        success &= manager.restore_backup(args.dotfiles)

    if args.delete_backup:
        success &= manager.delete_backup(args.dotfiles)

    if not success:
        print("Some operations completed with errors")
        sys.exit(1)
    else:
        print("All operations completed successfully")


if __name__ == "__main__":
    main()
