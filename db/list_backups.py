import boto3
from datetime import datetime

def list_rds_backups():
    try:
        # Crear cliente RDS
        rds = boto3.client('rds')
        
        print("\n📋 Lista de Backups Disponibles")
        print("=" * 50)
        
        # Listar snapshots automáticos
        auto_snapshots = rds.describe_db_snapshots(
            DBInstanceIdentifier='evo-sim-db',
            SnapshotType='automated'
        )
        
        print("\n🤖 Backups Automáticos:")
        for snapshot in auto_snapshots['DBSnapshots']:
            print(f"- {snapshot['DBSnapshotIdentifier']}")
            print(f"  Creado: {snapshot['SnapshotCreateTime']}")
            print(f"  Tamaño: {snapshot['AllocatedStorage']} GB")
            print("-" * 30)
            
        # Listar snapshots manuales
        manual_snapshots = rds.describe_db_snapshots(
            DBInstanceIdentifier='evo-sim-db',
            SnapshotType='manual'
        )
        
        print("\n👤 Backups Manuales:")
        for snapshot in manual_snapshots['DBSnapshots']:
            print(f"- {snapshot['DBSnapshotIdentifier']}")
            print(f"  Creado: {snapshot['SnapshotCreateTime']}")
            print(f"  Tamaño: {snapshot['AllocatedStorage']} GB")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Error al listar backups: {str(e)}")

if __name__ == '__main__':
    list_rds_backups()