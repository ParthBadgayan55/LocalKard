"""
LocalKard Backup Manager
Automated backup system for data protection
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import config

# ============================================================================
# BACKUP FUNCTIONS
# ============================================================================

def create_backup(source_dir: Path, backup_name: str = None) -> Path:
    """
    Create a backup of a directory

    Args:
        source_dir: Directory to backup
        backup_name: Optional custom backup name

    Returns:
        Path to created backup
    """
    if backup_name is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{source_dir.name}_{timestamp}"

    backup_path = config.BACKUP_DIR / backup_name

    # Copy entire directory
    shutil.copytree(source_dir, backup_path, dirs_exist_ok=True)

    return backup_path


def create_full_backup() -> Dict[str, Path]:
    """
    Create full backup of all data

    Returns:
        Dictionary mapping backup type to backup path
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backups = {}

    # Backup merchant data
    if config.DATA_DIR.exists():
        merchant_backup = create_backup(
            config.DATA_DIR,
            f"merchant_data_{timestamp}"
        )
        backups['merchant'] = merchant_backup

    # Backup central data
    if config.CENTRAL_DATA_DIR.exists():
        central_backup = create_backup(
            config.CENTRAL_DATA_DIR,
            f"central_data_{timestamp}"
        )
        backups['central'] = central_backup

    # Create backup manifest
    manifest = {
        'timestamp': timestamp,
        'datetime': datetime.now().isoformat(),
        'backups': {k: str(v) for k, v in backups.items()}
    }

    manifest_path = config.BACKUP_DIR / f"backup_manifest_{timestamp}.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    return backups


def list_backups() -> List[Dict[str, Any]]:
    """
    List all available backups

    Returns:
        List of backup information dictionaries
    """
    backups = []

    # Find all backup manifest files
    for manifest_file in config.BACKUP_DIR.glob('backup_manifest_*.json'):
        try:
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
                manifest['manifest_file'] = str(manifest_file)
                backups.append(manifest)
        except Exception as e:
            print(f"Error reading backup manifest {manifest_file}: {e}")

    # Sort by timestamp (newest first)
    backups.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

    return backups


def cleanup_old_backups(keep_count: int = None):
    """
    Remove old backups, keeping only the most recent

    Args:
        keep_count: Number of backups to keep (uses config default if None)
    """
    if keep_count is None:
        keep_count = config.BACKUP_RETENTION_COUNT

    backups = list_backups()

    # Remove old backups beyond retention count
    for backup in backups[keep_count:]:
        try:
            # Remove backup directories
            for backup_path in backup.get('backups', {}).values():
                path = Path(backup_path)
                if path.exists() and path.is_dir():
                    shutil.rmtree(path)

            # Remove manifest file
            manifest_file = Path(backup['manifest_file'])
            if manifest_file.exists():
                manifest_file.unlink()

        except Exception as e:
            print(f"Error cleaning up backup: {e}")


def restore_backup(backup_timestamp: str) -> bool:
    """
    Restore from a specific backup

    Args:
        backup_timestamp: Timestamp of backup to restore

    Returns:
        True if successful, False otherwise
    """
    # Find backup manifest
    manifest_file = config.BACKUP_DIR / f"backup_manifest_{backup_timestamp}.json"

    if not manifest_file.exists():
        print(f"Backup not found: {backup_timestamp}")
        return False

    try:
        with open(manifest_file, 'r') as f:
            manifest = json.load(f)

        # Restore each backup
        for backup_type, backup_path in manifest.get('backups', {}).items():
            source = Path(backup_path)

            if backup_type == 'merchant':
                destination = config.DATA_DIR
            elif backup_type == 'central':
                destination = config.CENTRAL_DATA_DIR
            else:
                continue

            if source.exists():
                # Remove existing data
                if destination.exists():
                    shutil.rmtree(destination)

                # Copy backup
                shutil.copytree(source, destination)

        print(f"Successfully restored backup from {backup_timestamp}")
        return True

    except Exception as e:
        print(f"Error restoring backup: {e}")
        return False


def get_backup_size(backup_timestamp: str) -> int:
    """
    Get total size of a backup in bytes

    Args:
        backup_timestamp: Timestamp of backup

    Returns:
        Size in bytes
    """
    manifest_file = config.BACKUP_DIR / f"backup_manifest_{backup_timestamp}.json"

    if not manifest_file.exists():
        return 0

    try:
        with open(manifest_file, 'r') as f:
            manifest = json.load(f)

        total_size = 0
        for backup_path in manifest.get('backups', {}).values():
            path = Path(backup_path)
            if path.exists() and path.is_dir():
                total_size += sum(f.stat().st_size for f in path.rglob('*') if f.is_file())

        return total_size

    except Exception as e:
        print(f"Error calculating backup size: {e}")
        return 0


# ============================================================================
# AUTOMATED BACKUP
# ============================================================================

def should_create_backup() -> bool:
    """
    Check if it's time to create a new backup

    Returns:
        True if backup should be created
    """
    if not config.BACKUP_ENABLED:
        return False

    backups = list_backups()

    if not backups:
        # No backups exist, create one
        return True

    # Check time since last backup
    last_backup = backups[0]
    last_backup_time = datetime.fromisoformat(last_backup['datetime'])
    hours_since_backup = (datetime.now() - last_backup_time).total_seconds() / 3600

    return hours_since_backup >= config.BACKUP_FREQUENCY_HOURS


def run_automated_backup():
    """
    Run automated backup if needed
    """
    if should_create_backup():
        print("Creating automated backup...")
        create_full_backup()
        cleanup_old_backups()
        print("Automated backup complete")


# ============================================================================
# EXPORT ALL
# ============================================================================

__all__ = [
    'create_backup',
    'create_full_backup',
    'list_backups',
    'cleanup_old_backups',
    'restore_backup',
    'get_backup_size',
    'should_create_backup',
    'run_automated_backup'
]
