# s3push-to-wochit

Sample project to automatically process dpa articles received via s3push-API. New or updated dpa articles are directly transferred to the S3-Bucket you own, converted from the dpa-digitalwires JSON to wochit-API-format and are sent to the wochit-API.

## TL;DR

Add wochit API credentials to the AWS SSM-Parameterstore:

- /dpa_import/wochit_api_key
- /dpa_import/wochit_client_id
- /dpa_import/wochit_client_secret

```
# please ensure aws-credentials are set to admin-user of your aws-account
npm install

nano serverless.yml   # please look for "CHANGE THIS" to change bucket names and prefix

npm run s3push-deploy

# please use the output to setup delivery in the dpa API-Portal
```

## Setup

Install dependencies by running `npm install` and `pip install -r requirements.txt`. For more details please check our generic [dpa-digitalwires-s3push-example](https://github.com/dpa-newslab/dpa-digitalwires-s3push-example/tree/main).

## Test

Running `npm run test` will convert all digitalwires-entries placed in `test/input` to the wochit-API-format. Output will be saved to `test/output`.

## Deployment

Save wochit-API client id and secret as SecureString to AWS SSM (`/dpa_import/wochit_api_key`, `/dpa_import/wochit_client_id` and `/dpa_import/wochit_client_secret`).

Adjust the `serverless.yml` file to your needs (mind the `CHANGE THIS!` comments).

Deploy to AWS:

```
npm run s3push-deploy
```

If the installation is successful, the following output appears:

```
Stack Outputs
S3PushSecretAccessKey: xxxx
S3PushUrlPrefix: s3://<s3_s3push_bucket_name>/<s3_s3push_prefix>
S3PushAccessKeyId: AKIAIxxxxx
... 
```

To set up the delivery, either contact your contact person at dpa or configure the API in the [customer portal](https://api-portal.dpa-newslab.com/).

For more details please check our generic [dpa-digitalwires-s3push-example](https://github.com/dpa-newslab/dpa-digitalwires-s3push-example/tree/main).