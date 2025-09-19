#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# CENTRAL CONFIGURATION - Easy to modify
DOTFILES_CONFIG = {
    "alacritty": {
        "system": "~/.config/alacritty/",
        "repo": "./alacritty/"
    },
    "fastfetch": {
        "system": "~/.config/fastfetch/",
        "repo": "./fastfetch/"
    },
    "fish": {
        "system": "~/.config/fish/",
        "repo": "./fish/"
    },
    "hypr": {
        "system": "~/.config/hypr/",
        "repo": "./hypr/"
    },
    "kitty": {
        "system": "~/.config/kitty/",
        "repo": "./kitty/"
    },
    "nvim": {
        "system": "~/.config/nvim/",
        "repo": "./nvim/"
    },
    "oh-my-posh": {
        "system": "~/.config/oh-my-posh/",
        "repo": "./oh-my-posh/"
    },
    "rofi": {
        "system": "~/.config/rofi",
        "repo": "./rofi/"
    },
    "waybar": {
        "system": "~/.config/waybar",
        "repo": "./waybar/"
    }
}


class DotfileManager:
    """Main class for managing dotfile synchronization and backups"""
    
    def __init__(self, config: Dict[str, Dict[str, str]], dry_run: bool = False):
        """
        Initialize the dotfile manager with configuration
        
        Args:
            config: Dictionary mapping dotfile names to system/repo paths
            dry_run: If True, show what would be done without executing
        """
        self.script_dir = Path(__file__).parent.absolute()
        self.config = self._expand_paths(config)
        self.dry_run = dry_run
        
    def _expand_paths(self, config: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, Path]]:
        """
        Expand user paths and convert strings to Path objects
        
        Args:
            config: Raw configuration with string paths
            
        Returns:
            Configuration with expanded Path objects
        """
        expanded = {}
        for name, paths in config.items():
            expanded[name] = {
                "system": Path(paths["system"]).expanduser().resolve(),
                "repo": (self.script_dir / paths["repo"].lstrip("./")),
            }
        return expanded
    
    def _confirm_operation(self, message: str) -> bool:
        """
        Ask user for confirmation
        
        Args:
            message: Message to display
            
        Returns:
            True if user confirms, False otherwise
        """
        if self.dry_run:
            return True
            
        while True:
            response = input(f"{message} [y/N]: ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no', '']:
                return False
            else:
                print("Please enter 'y' or 'n'")
    
    def _run_rsync(self, source: Path, dest: Path, description: str, delete_extra: bool = False) -> bool:
        """
        Run rsync command with proper options
        
        Args:
            source: Source path
            dest: Destination path  
            description: Description for logging
            delete_extra: Whether to delete files in dest that don't exist in source
            
        Returns:
            True if successful, False otherwise
        """
        # Create destination parent directory if it doesn't exist
        if not self.dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
        
        # Build rsync command
        rsync_args = ["rsync", "-avh", "--progress"]
        
        if delete_extra:
            rsync_args.append("--delete")
            
        if self.dry_run:
            rsync_args.append("--dry-run")
        
        # Ensure proper trailing slash handling for directories
        source_str = str(source).rstrip('/') + '/'
        dest_str = str(dest).rstrip('/') + '/'
        
        rsync_args.extend([source_str, dest_str])
        
        print(f"{description}: {source} -> {dest}")
        if delete_extra:
            print("  WARNING: Files in destination not present in source will be DELETED")
        if self.dry_run:
            print("  [DRY RUN - no changes will be made]")
        
        try:
            result = subprocess.run(rsync_args, check=True, capture_output=True, text=True)
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
    
    def deploy(self, dotfiles: Optional[List[str]] = None) -> bool:
        """
        Deploy dotfiles from repository to system locations
        
        Args:
            dotfiles: List of specific dotfiles to deploy. If None, deploy all.
            
        Returns:
            True if all operations successful
        """
        print("Deploying dotfiles from repository to system...")
        
        target_dotfiles = dotfiles if dotfiles else list(self.config.keys())
        
        # Show what will be deployed
        print("\nFiles to deploy:")
        for name in target_dotfiles:
            if name not in self.config:
                print(f"  WARNING: '{name}' not found in configuration")
                continue
            paths = self.config[name]
            print(f"  {name}: {paths['repo']} -> {paths['system']}")
        
        if not self._confirm_operation("\nProceed with deployment?"):
            print("Deployment cancelled.")
            return False
        
        success = True
        
        for name in target_dotfiles:
            if name not in self.config:
                continue
                
            paths = self.config[name]
            
            if not paths["repo"].exists():
                print(f"Warning: Repository directory {paths['repo']} doesn't exist, skipping {name}")
                continue
                
            if not self._run_rsync(paths["repo"], paths["system"], f"Deploying {name}", delete_extra=True):
                success = False
                
        return success
    
    def retrieve(self, dotfiles: Optional[List[str]] = None) -> bool:
        """
        Retrieve dotfiles from system to repository

        Args:
            dotfiles: List of specific dotfiles to retrieve. If None, retrieve all.

        Returns:
            True if all operations successful
        """
        print("Retrieving dotfiles from system to repository...")

        target_dotfiles = dotfiles if dotfiles else list(self.config.keys())

        # Show what will be retrieved and check for potential issues
        print("\nFiles to retrieve:")
        warnings = []
        for name in target_dotfiles:
            if name not in self.config:
                print(f"  WARNING: '{name}' not found in configuration")
                continue
            paths = self.config[name]

            # Safety check: warn if system doesn't exist but repo does
            if not paths["system"].exists():
                if paths["repo"].exists():
                    warnings.append(f"  DANGER: {name} - System directory missing but repo has content!")
                    print(f"  {name}: {paths['system']} -> {paths['repo']} (SYSTEM MISSING - WOULD DELETE REPO CONTENT)")
                else:
                    print(f"  {name}: {paths['system']} -> {paths['repo']} (both missing)")
            else:
                print(f"  {name}: {paths['system']} -> {paths['repo']}")

        # Show warnings if any
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

            if not paths["system"].exists():
                # Extra safety: skip if system doesn't exist and repo does
                if paths["repo"].exists():
                    print(f"SKIPPING {name}: System directory doesn't exist but repo has content - preserving repo")
                    continue
                else:
                    print(f"Warning: System directory {paths['system']} doesn't exist, skipping {name}")
                    continue
                
            if not self._run_rsync(paths["system"], paths["repo"], f"Retrieving {name}", delete_extra=True):
                success = False

        return success
    
    def create_backup(self, dotfiles: Optional[List[str]] = None) -> bool:
        """
        Create backup copies of system files
        
        Args:
            dotfiles: List of specific dotfiles to backup. If None, backup all.
            
        Returns:
            True if all operations successful
        """
        print("Creating backups of system files...")
        
        target_dotfiles = dotfiles if dotfiles else list(self.config.keys())
        
        # Show what will be backed up
        print("\nFiles to backup:")
        for name in target_dotfiles:
            if name not in self.config:
                print(f"  WARNING: '{name}' not found in configuration")
                continue
            paths = self.config[name]
            backup_path = Path(str(paths["system"]) + ".bak")
            print(f"  {name}: {paths['system']} -> {backup_path}")
        
        if not self._confirm_operation("\nProceed with backup creation?"):
            print("Backup cancelled.")
            return False
        
        success = True
        
        for name in target_dotfiles:
            if name not in self.config:
                continue
                
            paths = self.config[name]
            system_path = paths["system"]
            backup_path = Path(str(system_path) + ".bak")
            
            if not system_path.exists():
                print(f"Warning: System directory {system_path} doesn't exist, skipping {name}")
                continue
                
            if backup_path.exists() and not self.dry_run:
                print(f"Warning: Backup {backup_path} already exists, skipping {name}")
                continue
                
            if not self._run_rsync(system_path, backup_path, f"Backing up {name}"):
                success = False
                
        return success
    
    def restore_backup(self, dotfiles: Optional[List[str]] = None) -> bool:
        """
        Restore files from backup copies
        
        Args:
            dotfiles: List of specific dotfiles to restore. If None, restore all.
            
        Returns:
            True if all operations successful
        """
        print("Restoring from backup files...")
        
        target_dotfiles = dotfiles if dotfiles else list(self.config.keys())
        
        # Show what will be restored
        print("\nFiles to restore:")
        for name in target_dotfiles:
            if name not in self.config:
                print(f"  WARNING: '{name}' not found in configuration")
                continue
            paths = self.config[name]
            backup_path = Path(str(paths["system"]) + ".bak")
            print(f"  {name}: {backup_path} -> {paths['system']}")
        
        if not self._confirm_operation("\nProceed with restore?"):
            print("Restore cancelled.")
            return False
        
        success = True
        
        for name in target_dotfiles:
            if name not in self.config:
                continue
                
            paths = self.config[name]
            system_path = paths["system"]
            backup_path = Path(str(system_path) + ".bak")
            
            if not backup_path.exists():
                print(f"Warning: Backup file {backup_path} doesn't exist, skipping {name}")
                continue
                
            if not self._run_rsync(backup_path, system_path, f"Restoring {name}", delete_extra=True):
                success = False
                
        return success
    
    def delete_backup(self, dotfiles: Optional[List[str]] = None) -> bool:
        """
        Delete backup files
        
        Args:
            dotfiles: List of specific dotfile backups to delete. If None, delete all.
            
        Returns:
            True if all operations successful
        """
        print("Deleting backup files...")
        
        target_dotfiles = dotfiles if dotfiles else list(self.config.keys())
        
        # Show what will be deleted
        print("\nBackup files to delete:")
        backups_to_delete = []
        for name in target_dotfiles:
            if name not in self.config:
                print(f"  WARNING: '{name}' not found in configuration")
                continue
            paths = self.config[name]
            backup_path = Path(str(paths["system"]) + ".bak")
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
        """List all configured dotfiles with their paths"""
        print("Configured dotfiles:")
        for name, paths in self.config.items():
            system_exists = "EXISTS" if paths['system'].exists() else "MISSING"
            repo_exists = "EXISTS" if paths['repo'].exists() else "MISSING"
            
            print(f"  {name}:")
            print(f"    System: {paths['system']} ({system_exists})")
            print(f"    Repo:   {paths['repo']} ({repo_exists})")
            print()


def interactive_menu():
    """Show interactive menu when no arguments provided"""
    while True:
        print("\nDotfiles Manager - Interactive Mode")
        print("===================================")
        print("d. Deploy (repo -> system)")
        print("r. Retrieve (system -> repo)") 
        print("b. Create backup")
        print("R. Restore backup")
        print("D. Delete backup")
        print("l. List dotfiles")
        print("q. Exit")
        
        try:
            choice = input("\nSelect operation: ").strip()
            
            if choice == 'q':
                print("Goodbye!")
                break
            elif choice in ['d', 'r', 'b', 'R', 'D']:
                # Show available dotfiles
                print(f"\nAvailable dotfiles: {', '.join(DOTFILES_CONFIG.keys())}")
                selection = input("Enter dotfile names (space-separated, or press Enter for all): ").strip()
                dotfiles = selection.split() if selection else None
                
                # Validate selection
                if dotfiles:
                    invalid = set(dotfiles) - set(DOTFILES_CONFIG.keys())
                    if invalid:
                        print(f"Error: Unknown dotfiles: {', '.join(invalid)}")
                        continue
                
                dry_run = input("Dry run? [y/N]: ").lower().strip() in ['y', 'yes']
                
                manager = DotfileManager(DOTFILES_CONFIG, dry_run=dry_run)
                
                if choice == 'd':
                    manager.deploy(dotfiles)
                elif choice == 'r':
                    manager.retrieve(dotfiles)
                elif choice == 'b':
                    manager.create_backup(dotfiles)
                elif choice == 'R':
                    manager.restore_backup(dotfiles)
                elif choice == 'D':
                    manager.delete_backup(dotfiles)
                    
            elif choice == 'l':
                manager = DotfileManager(DOTFILES_CONFIG)
                manager.list_dotfiles()
            else:
                print("Invalid choice. Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""
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
    
    # Target specific dotfiles
    parser.add_argument(
        "dotfiles", 
        nargs="*",
        help="Specific dotfiles to operate on (default: all)"
    )
    
    return parser


def main():
    """Main entry point"""
    parser = create_argument_parser()
    
    # If no arguments, show interactive menu
    if len(sys.argv) == 1:
        interactive_menu()
        return
        
    args = parser.parse_args()
    
    # Initialize dotfile manager
    manager = DotfileManager(DOTFILES_CONFIG, dry_run=args.dry_run)
    
    # Handle list operation first
    if args.list:
        manager.list_dotfiles()
        return
    
    # Validate dotfile names if specified
    if args.dotfiles:
        invalid_dotfiles = set(args.dotfiles) - set(DOTFILES_CONFIG.keys())
        if invalid_dotfiles:
            print(f"Error: Unknown dotfiles: {', '.join(invalid_dotfiles)}")
            print(f"Available: {', '.join(DOTFILES_CONFIG.keys())}")
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
