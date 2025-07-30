import boto3

def lambda_handler(event, context):
    regions = []
    # Get a list of all regions
    ec2_client = boto3.client('ec2')
    regions_response = ec2_client.describe_regions()
    for region in regions_response['Regions']:
        regions.append(region['RegionName'])

    snapshots_created = []
    # Iterate through each region
    for region in regions:
        print(f"Processing region: {region}")
        ec2 = boto3.client('ec2', region_name=region)
        # Get all volumes in 'in-use' state
        volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['in-use']}])['Volumes']
        for volume in volumes:
            volume_id = volume['VolumeId']
            print(f"Creating snapshot for Volume: {volume_id}")
            # Create a snapshot
            try:
                snapshot = ec2.create_snapshot(
                    VolumeId=volume_id,
                    Description=f"Snapshot of {volume_id} from region {region}"
                )
                snapshots_created.append({
                    "Region": region,
                    "VolumeId": volume_id,
                    "SnapshotId": snapshot['SnapshotId']
                })
                print(f"Snapshot created: {snapshot['SnapshotId']}")
            except Exception as e:
                print(f"Error creating snapshot for volume {volume_id} in region {region}: {str(e)}")

    return {
        "statusCode": 200,
        "body": f"Snapshots created: {snapshots_created}"
    }

