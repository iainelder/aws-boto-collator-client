# AWS Boto Collator Client

A wrapper for a boto3 client that collates each paginated API call into a single result.

For anything else, like non-method attributes or non-pagianted API methods, it returns the same result as the wrapped client.

The AWS CLI conveniently collates automatically. If you naively translate an AWS CLI command to to boto3 method call, you might be surprised when you get less results than you were expecting for a long list of resources.

Use this wrapper to collate automatically whenever it would be necessary to get the full result.

## Example

To use it, just wrap a normal boto3 client in with the CollatorClient constructor.

```python
import boto3

from collator_client import CollatorClient

org = boto3.Session().client("organizations")

collated_org = CollatorClient(org)

len(org.list_accounts()["Accounts"])

len(collated_org.list_accounts()["Accounts"])
```

Example output in IPython in an organization with more than 20 accounts:

```text
In [5]: len(org.list_accounts()["Accounts"])
Out[5]: 20

In [6]: len(collated_org.list_accounts()["Accounts"])
Out[6]: 45
```

