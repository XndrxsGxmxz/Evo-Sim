import boto3

def check_backup_settings():
    try:
        rds = boto3.client('rds')
        
        # Obtener configuración de la instancia
        response = rds.describe_db_instances(
            DBInstanceIdentifier='evo-sim-db'
        )
        
        instance = response['DBInstances'][0]
        
        print("\n Configuración de Backups")
        print("=" * 50)
        print(f"• Periodo de retención: {instance['BackupRetentionPeriod']} días")
        print(f"• Ventana de backup: {instance['PreferredBackupWindow']}")
        print(f"• Último backup: {instance['LatestRestorableTime']}")
        
    except Exception as e:
        print(f" Error: {str(e)}")

if __name__ == '__main__':
    check_backup_settings()