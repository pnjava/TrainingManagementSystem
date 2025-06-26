import { App } from 'aws-cdk-lib';
import { CoreNetworkStack } from '../lib/core-network';

const app = new App();

new CoreNetworkStack(app, 'CoreNetworkStack', {
  env: { region: 'us-east-1' },
});
