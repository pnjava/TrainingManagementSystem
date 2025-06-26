import { Stack, StackProps, Tags } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Bucket, BlockPublicAccess } from 'aws-cdk-lib/aws-s3';
import { Distribution, OriginAccessIdentity, ViewerProtocolPolicy } from 'aws-cdk-lib/aws-cloudfront';
import { S3Origin } from 'aws-cdk-lib/aws-cloudfront-origins';
import { Vpc, SubnetType } from 'aws-cdk-lib/aws-ec2';

export class CoreNetworkStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    Tags.of(this).add('Application', 'CTTS');
    Tags.of(this).add('Env', 'DevInt');
    Tags.of(this).add('Owner', 'BEA');
    Tags.of(this).add('DataGovernor', 'CDO');
    Tags.of(this).add('Compliance', 'Sec530');
    Tags.of(this).add('PII', 'No');

    const vpc = Vpc.fromLookup(this, 'ImportedVpc', { vpcId: 'vpc-xxxxxxxx' });

    const privateSubnet = { subnetType: SubnetType.PRIVATE_WITH_EGRESS };
    const publicSubnet = { subnetType: SubnetType.PUBLIC };

    const spaBucket = new Bucket(this, 'SpaBucket', {
      bucketName: 'ctts-spa-devint',
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
      versioned: true,
    });

    const oai = new OriginAccessIdentity(this, 'OAI');

    const distribution = new Distribution(this, 'SpaDistribution', {
      defaultBehavior: {
        origin: new S3Origin(spaBucket, { originAccessIdentity: oai }),
        viewerProtocolPolicy: ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
      },
      domainNames: ['apps-d.dbhds.virginia.gov'],
    });

    this.exportValue(spaBucket.bucketName, { name: 'SpaBucketName' });
    this.exportValue(distribution.domainName, { name: 'SpaCfDomain' });
  }
}
