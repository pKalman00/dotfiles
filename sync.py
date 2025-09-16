import os, sys, subprocess, argparse

class Sync:
    def __init__(self, paths):
        self.paths = paths
    
    def retrieve(self):
        print("Retrieving dotfiles from system to repo...")
        for paths in self.paths.values():
            print(subprocess.run(["rsync", "-arvz", paths["system"], paths["repo"]], capture_output=True).stdout.decode())
            
    def deploy(self):
        print("Deploying dotfiles from repo to system...")
        for paths in self.paths.values():
            print(subprocess.run(["rsync", "-arvz", paths["repo"], paths["system"]], capture_output=True).stdout.decode())
    
class Backup(Sync):
    def __init__(self, paths):
        self.paths = paths
    
    def create(self):
        print("Creating backups of existing system files...")
        for paths in self.paths.values():
            print(subprocess.run(["rsync", "-arvz", paths["system"], f"{paths["system"]}.bak"], capture_output=True).stdout.decode())
    
    def restore(self):
        print("Restoring from .bak backup files...")
        for paths in self.paths.values():
            print(subprocess.run(["rsync", "-arvz", f"{paths["system"]}.bak", paths["system"]], capture_output=True).stdout.decode())
    
    def delete(self):
        print("Deleting .bak backup files...")
        for paths in self.paths.values():
            if os.path.exists(f"{paths['system']}.bak"):
                print(subprocess.run(["rm", "-r", f"{paths["system"]}.bak"]))
                print(f"Deleted {paths['system']}")
            else:
                print(f"{paths['system']}.bak does not exist")

class Setup:
    def __init__(self):
        self.argparse()
        self.paths = {
            "alacritty": {
                "system": os.path.expanduser("~/.config/alacritty/alacritty.toml"),
                "repo": "./alacritty/alacritty.toml"
            },
            "fastfetch": {
                "system": os.path.expanduser("~/.config/fastfetch/config.jsonc"),
                "repo": "./fastfetch/config.jsonc"
            },
            "fish": {
                "system": os.path.expanduser("~/.config/fish/config.fish"),
                "repo": "./fish/config.fish"
            },
            "fish_functions": {
                "system": os.path.expanduser("~/.config/fish/functions/"),
                "repo": "./fish/functions/"
            },
            "oh-my-posh": {
                "system": os.path.expanduser("~/.config/oh-my-posh/omp.json"),
                "repo": "./oh-my-posh/omp.json"
            },
            "nvim": {
                "system": os.path.expanduser("~/.config/"),
                "repo": "./nvim"
            }
            
            # more
        }
        
        
        
    def argparse(self):
        parser = argparse.ArgumentParser(description="Sync dotfiles")
        parser.add_argument("-r", "--retrieve", action="store_true", help="Retrieve dotfiles from system to repo")
        parser.add_argument("-d", "--deploy", action="store_true", help="Deploy dotfiles from repo to system")
        parser.add_argument("-b", "--backup", action="store_true", help="Create backups of existing system files")
        parser.add_argument("-R", "--restore", action="store_true", help="Restore from .bak backup files")
        parser.add_argument("-D", "--delete", action="store_true", help="Delete .bak backup files")
        if len(sys.argv) == 1:
            parser.print_help()
            exit(2)
        self.args = parser.parse_args()
        
if __name__ == "__main__":
    setup = Setup()
    sync = Sync(setup.paths)
    bak = Backup(setup.paths)
    
    if setup.args.retrieve:
        sync.retrieve()
        
    if setup.args.deploy:
        sync.deploy()
    
    if setup.args.backup:
        bak.create()
    
    if setup.args.restore:
        bak.restore()
    
    if setup.args.delete:
        bak.delete()
